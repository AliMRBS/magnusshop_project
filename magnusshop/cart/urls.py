from django.urls import path
from . import views


urlpatterns = [
    path('', views.CartSummaryView.as_view(), name="cart-summary"),
    path('add/', views.CartAddView.as_view(), name="cart-add"),
    path('delete/', views.CartDeleteView.as_view(), name="cart-delete"),
    path('update/', views.CartUpdateView.as_view(), name="cart-update"),

]