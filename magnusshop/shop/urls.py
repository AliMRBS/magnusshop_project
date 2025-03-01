from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.ProductListView, name="product-list"),
    path('off/', views.OffProductListView, name="product-off"),
    path('search/', views.ProductSearchView, name="product-search"),
    path('about/', TemplateView.as_view(template_name="about.html"), name="about-us"),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name="product-detail"),
    path('product/<int:pk>/comment/', views.SaveProductCommentView.as_view(), name="product-comment"),
    path('category/<int:pk>', views.CategoryProductView, name="category-product"),

]