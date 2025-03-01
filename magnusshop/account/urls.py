from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.LogInView, name="login"),
    path('logout/', views.LogOutView, name="logout"),
    path('signup/', views.SignUpView, name="signup"),
    path("verify-email/<int:user_id>/", views.VerifyEmailView, name="verify-email"),
    
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/<int:user_id>/', views.VerifyOTPForPasswordView.as_view(), name='verify-otp'),
    path('reset-password/<int:user_id>/', views.ResetPasswordView.as_view(), name='reset-password'),

    path('', views.ProfileView.as_view(), name="profile"),
    path('info/', views.ProfileInfoView.as_view(), name="profile-info"),
    path('order/', views.ProfileOrderView.as_view(), name="profile-order"),

    path('address/', views.AddressListView.as_view(), name='address'),
    path('address/add/', views.AddressCreateView.as_view(), name='add-address'),
    path('address/edit/<int:pk>/', views.AddressUpdateView.as_view(), name='edit-address'),
    path('address/delete/<int:pk>/', views.AddressDeleteView.as_view(), name='delete-address'),

    path('magnusplus/', views.ProfileMagnusPlusView.as_view(), name="profile-magnusplus"),
]