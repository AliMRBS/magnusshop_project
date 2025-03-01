from django.shortcuts import redirect, render
from .models import Category, Product, ProductComment
from django.db.models import Q
from django.contrib import messages
import random
from django.shortcuts import get_object_or_404
from .forms import ProductCommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random

def ProductListView(request):
    sort = request.GET.get('sort', '')
    page = request.GET.get('page', 1)

    valid_sort_options = {
        'price-asc': 'price',
        'price-desc': '-price',
        'newest': '-create_time'
    }
    order_by = valid_sort_options.get(sort, '-create_time')

    cache_key = f"products_{sort}_page{page}"
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.select_related('category').prefetch_related('images').order_by(order_by)
        paginator = Paginator(products, 20)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        cache.set(cache_key, products, timeout=60 * 10) 

    categories = cache.get("categories")
    if not categories:
        categories = Category.objects.all()
        cache.set("categories", categories, timeout=60 * 60) 

    sale_products = cache.get("sale_products")
    if not sale_products:
        sale_products = Product.objects.filter(is_sale=True, is_active=True)
        cache.set("sale_products", sale_products, timeout=60 * 30) 

    random_product = random.choice(sale_products) if sale_products else None

    discount = 0
    if random_product and random_product.price > 0:
        discount = 100 * (1 - (random_product.sale_price / random_product.price))

    queryset_products = Product.objects.filter(is_active=True).order_by('-create_time')[:10]

    return render(request, 'product_list.html', {
        'queryset_products':queryset_products,
        'products': products,
        'categories': categories,
        'random_product': random_product,
        'discount': int(discount),
        'sort': sort
    })


def OffProductListView(request):
    sort = request.GET.get('sort', '')
    page = request.GET.get('page', 1)

    valid_sort_options = {
        'price-asc': 'price',
        'price-desc': '-price',
        'newest': '-create_time'
    }
    order_by = valid_sort_options.get(sort, '-create_time')

    cache_key = f"products_{sort}_page{page}"
    products = cache.get(cache_key)  

    if not products:
        queryset = Product.objects.filter(is_sale=True, is_active=True).select_related('category').prefetch_related('images').order_by(order_by)

        paginator = Paginator(queryset, 20)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        cache.set(cache_key, products, timeout=300)

    categories = cache.get('categories')  
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, timeout=300)  


    return render(request, 'offs.html', {
        'products': products,
        'categories': categories,
        'sort': sort
    })


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product.objects.filter(is_active=True).select_related('category').prefetch_related('images'), Q(pk=pk) | Q(upc=pk))

        queryset_products = Product.objects.filter(
            Q(title__icontains=product.title) | Q(category=product.category)
        ).exclude(pk=product.pk)[:10] 

        comments = ProductComment.objects.filter(product=product)

        form = ProductCommentForm()
        return render(request, 'product_detail.html', {'queryset_products': queryset_products, 'product': product, 'form': form, 'comments': comments})


class SaveProductCommentView(LoginRequiredMixin, View):
    login_url = 'account:login'  
    redirect_field_name = 'next'  

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductCommentForm()
        comments = ProductComment.objects.filter(product=product)

        return render(request, 'product_detail.html', {'product': product, 'form': form, 'comments': comments})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductCommentForm(request.POST)

        if form.is_valid():
            product_comment = form.save(commit=False)
            product_comment.product = product  
            product_comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
            return redirect('product-detail', pk=product.pk)
        else:
            messages.error(request, 'خطا در ثبت نظر')
        comments = ProductComment.objects.filter(product=product)
        return render(request, 'product_detail.html', {'product': product, 'form': form, 'comments': comments})


def CategoryProductView(request, pk):
    category = get_object_or_404(Category, pk=pk)

    sort = request.GET.get('sort')
    cache_key = f"category_{category.pk}_sort_{sort}"

    products = cache.get(cache_key)

    if not products:
        products = Product.objects.filter(category=category).select_related('category').prefetch_related('images')

        if sort == 'price-asc':
            products = products.order_by('price')
        elif sort == 'price-desc':
            products = products.order_by('-price')
        elif sort == 'newest':
            products = products.order_by('-create_time')

        cache.set(cache_key, products, timeout=3600)

    return render(request, 'product_list.html', {'products': products})


def ProductSearchView(request):
    searched = request.GET.get('searched', '')
    sort_param = request.GET.get('sort', '')

    cache_key = f"search_{searched}_sort_{sort_param}"

    searched_products = cache.get(cache_key)

    if not searched_products:
        searched_products = Product.objects.all().select_related('category').prefetch_related('images')

        if searched:
            searched_products = searched_products.filter(title__icontains=searched)

        if sort_param == 'price-asc':
            searched_products = searched_products.order_by('price')
        elif sort_param == 'price-desc':
            searched_products = searched_products.order_by('-price')
        elif sort_param == 'newest':
            searched_products = searched_products.order_by('-create_time')

        cache.set(cache_key, searched_products, timeout=3600)

    if not searched_products.exists():
        messages.success(request, "محصول مورد نظر یافت نشد")
        return redirect('product-list')

    all_products = Product.objects.select_related('category').prefetch_related('images')

    return render(request, 'product_list.html', {
        'all_products': all_products,
        "products": searched_products,
        "searched": searched,
        "sort": sort_param  
    })

