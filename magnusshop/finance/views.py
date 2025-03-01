from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from payment.models import Order
from finance.models import Payment
from cart.cart import Cart
from django.db import transaction
from account.models import Profile


class PayOrderView(View):
    def post(self, request, id, *args, **kwargs):
        try:
            order = Order.objects.get(id=id, profile=request.user.profile)
        except Order.DoesNotExist:
            return HttpResponse("سفارش مورد نظر یافت نشد.", status=404)

        if order.status != 'pending':
            return HttpResponse("این سفارش قابل پرداخت نیست.", status=400)

        payment = Payment(
            amount=order.total_amount,
            gateway=Payment.get_gateway(),  
            user=request.user,
        )
        payment.save_log(data=f"Payment initialized: Amount={payment.amount}, Gateway={payment.gateway}", scope="PayOrder - Initialize Payment")

        redirect_url = payment.bank_page
        if redirect_url:
            with transaction.atomic():
                payment.save()  
                order.payment = payment
                order.save()  
                payment.save_log(data=f"Payment and Order saved: Payment ID={payment.id}, Order ID={order.id}", scope="PayOrder - Save Payment and Order")
            return redirect(redirect_url)
        
        payment.save_log(data="Error connecting to payment gateway.", scope="PayOrder - Gateway Error")
        return HttpResponse("خطا در ارتباط با درگاه پرداخت.", status=500)

    

@method_decorator(csrf_exempt, name='dispatch')
class VerfiyPaymentView(View):
    template_name = 'callback.html'

    def post(self, request, *args, **kwargs):
        transid = request.POST.get('transid')
        

        try:
            payment = Payment.objects.get(transid=transid)
            payment.save_log(data=f"Payment found: ID={payment.id}, Amount={payment.amount}", scope="VerifyPayment - Fetch Payment")
        except Payment.DoesNotExist:
            Payment.save_log(None, data=f"Payment not found: transid={transid}", scope="VerifyPayment - Error", save=False)
            raise Http404

        is_paid = payment.verify({'transid': transid, 'amount': payment.amount})
        payment.save_log(data=f"Verification result: {'Success' if is_paid else 'Failure'}", scope="VerifyPayment - Verification Result")

        if is_paid:
            cart = Cart(request)
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            user_profile = get_object_or_404(Profile, user=request.user)
            user_profile.old_cart = None 
            user_profile.save()
            
            payment.save_log(data="Session cleared after successful payment.", scope="VerifyPayment - Session Clearing")

        context = {
            'amount': payment.amount,
            'transid': payment.transid,
            'is_paid': is_paid,
        }
        return render(request, self.template_name, context)
