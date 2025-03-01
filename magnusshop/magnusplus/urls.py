from django.urls import path
from . import views


app_name = 'magnusplus'

urlpatterns = [
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('purchase/', views.PurchaseSubscriptionView.as_view(), name='purchase-subscription'),

    
]