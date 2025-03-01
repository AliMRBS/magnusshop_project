from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product

class CartSummaryView(View):
    def get(self, request):
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quants()
        total_price = cart.get_total()
        return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'total_price': total_price})


@method_decorator(require_POST, name='dispatch')
class CartAddView(View):
    def post(self, request):
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not product_id or not product_qty:
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
            if product_qty <= 0:
                return JsonResponse({'error': 'Invalid quantity'}, status=400)

            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)

            messages.success(request, 'محصول به سبد خرید اضافه شد')
            return JsonResponse({'qty': cart.__len__()})

        except ValueError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)


@method_decorator(require_POST, name='dispatch')
class CartUpdateView(View):
    def post(self, request):
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not product_id or not product_qty:
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
            if product_qty <= 0:
                return JsonResponse({'error': 'Invalid quantity'}, status=400)

            cart.update(product=product_id, quantity=product_qty)
            messages.success(request, 'تعداد محصول تغییر یافت')

            return JsonResponse({'qty': product_qty})

        except ValueError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)


@method_decorator(require_POST, name='dispatch')
class CartDeleteView(View):
    def post(self, request):
        cart = Cart(request)
        product_id = request.POST.get('product_id')

        if not product_id:
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            product_id = int(product_id)
            cart.delete(product=product_id)
            messages.success(request, 'محصول از سبد خرید حذف شد')

            return JsonResponse({'product': product_id})

        except ValueError:
            return JsonResponse({'error': 'Invalid data format'}, status=400)
