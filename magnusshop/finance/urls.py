
from django.urls import path
from . import views
app_name = 'finance' 


urlpatterns = [
    path('pay/<int:id>/', views.PayOrderView.as_view(), name='pay-order'),
    path('verify/', views.VerfiyPaymentView.as_view(), name='verify-payment'),

]