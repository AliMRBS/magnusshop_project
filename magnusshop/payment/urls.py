from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('shipping_address/', views.ShippingAddressListView.as_view(), name="shipping-address"),
    path('add_address/', views.AddressCreateView.as_view(), name='add-address'),
    path('edit_address/<int:pk>/', views.AddressUpdateView.as_view(), name='edit-address'),
    path('save_shipping_address/', views.ShippingAddressSaveView.as_view(), name='save-shipping-address'),
    path('basket_detail/', views.BasketDetailView.as_view(), name='basket-detail'),
    path('create_order/', views.CreateOrderView.as_view(), name='create-order'),

]