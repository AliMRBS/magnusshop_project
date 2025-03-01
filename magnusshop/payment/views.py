from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from shop.models import Product
from account.models import Address
from account.forms import AddressUpdateForm
from .models import Order, OrderItem
from cart.cart import Cart  


class ShippingAddressListView(LoginRequiredMixin, View):
    login_url = 'account:login'  
    redirect_field_name = 'next'  

    def get(self, request):
        addresses = Address.objects.filter(profile__user=request.user)
        form = AddressUpdateForm()
        return render(request, 'shipping_address.html', {'addresses': addresses, 'form': form})
 

class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressUpdateForm
    
    def form_valid(self, form):
        address = form.save(commit=False)
        address.profile = self.request.user.profile
        address.save()
        messages.success(self.request, 'آدرس با موفقیت اضافه شد.')
        return JsonResponse({'message': 'آدرس با موفقیت اضافه شد.'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressUpdateForm

    def get_object(self, queryset=None):
        return Address.objects.get(id=self.kwargs['pk'], profile=self.request.user.profile)

    def form_valid(self, form):
        form.save()
        return JsonResponse({'message': 'آدرس با موفقیت به‌روزرسانی شد.'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class ShippingAddressSaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        address_id = request.POST.get('selected_address')
        if not address_id:
            return redirect('payment:shipping-address-error')  

        try:
            address = Address.objects.get(id=address_id, profile=request.user.profile)
        except Address.DoesNotExist:
            return redirect('payment:shipping-address-error') 

        request.session['selected_address'] = address_id

        return redirect('payment:basket-detail')
    


class BasketDetailView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        cart = Cart(request) 
        
        if not cart.get_quants():
            messages.warning(request, "سبد خرید شما خالی است!")
            return redirect('cart-summary') 

        cart_items = []
        for product_id, quantity in cart.get_quants().items():
            try:
                product = Product.objects.get(id=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price * quantity if not product.is_sale else product.sale_price * quantity,
                })
            except Product.DoesNotExist:
                continue

        address_id = request.session.get('selected_address')
        address = None
        if address_id:
            try:
                address = Address.objects.get(id=address_id, profile=request.user.profile)
            except Address.DoesNotExist:
                pass  

        context = {
            'cart': cart_items,
            'address': address,  
            'order_total': cart.get_total(),
        }
        return render(request, 'basket_detail.html', context)


class CreateOrderView(View):
    def post(self, request):
        shipping_address_id = request.session.get('selected_address')
        if not shipping_address_id:
            return JsonResponse({'error': 'آدرس ارسال انتخاب نشده است!'}, status=400)

        profile = request.user.profile
        cart = Cart(request)

        try:
            shipping_address = Address.objects.get(id=shipping_address_id, profile__user=request.user)
        except Address.DoesNotExist:
            return JsonResponse({'error': 'آدرس ارسال معتبر نیست!'}, status=400)

        order = Order.objects.create(
            profile=profile,
            full_name=f"{profile.first_name} {profile.last_name}".strip(),
            shipping_address=f"استان {shipping_address.province}، شهر {shipping_address.city}، {shipping_address.address}, پلاک {shipping_address.house_number}، واحد {shipping_address.unit_number}، کد پستی: {shipping_address.zipcode}".strip(),
            zipcode=shipping_address.zipcode,
            total_amount=cart.get_total(),
        )

        order_obj = get_object_or_404(Order, id=order.pk)
        
        for product in cart.get_products():
            product_obj = get_object_or_404(Product, id=product.id)

            if product.is_sale:
                unit_price = product.sale_price
            else:
                unit_price = product.price

            for key, value in cart.get_quants().items():
                if int(key) == product.id:
                    order_item = OrderItem.objects.create(
                        order=order_obj,
                        product=product_obj,
                        user=request.user,
                        quantity=value,
                        unit_price=unit_price,
                        total_price=unit_price*value,
                    )

        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return render(request, 'confirm_order.html', {'order': order})

    def get(self, request):
        messages.success(request, 'دسترسی به این صفحه امکان‌پذیر نمی‌باشد.')
        return JsonResponse({'error': 'دسترسی به این صفحه غیرمجاز است!'}, status=405)
