from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, Address
import json
from cart.cart import Cart
from .forms import SignUpForm, ProfileInfoForm, AddressUpdateForm
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from payment.models import Order
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .utils import send_otp_email


def LogInView(request):
    next_url = request.GET.get('next') 
    if request.method == 'POST':
        email  = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email , password=password)

        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)

                cart = Cart(request)

                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, 'با موفقیت وارد حساب کاربری شدید')

            next_url = request.POST.get('next', next_url)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            return redirect('product-list')  

        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
            return redirect('account:login')

    else:
        return render(request, 'login.html', {'next': next_url or '/'} ) 
    

@login_required
def LogOutView(request):
    logout(request)
    messages.success(request, ('با موفقیت خارج شدید'))
    return redirect('product-list')



def SignUpView(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
            return render(request, 'signup.html', {'form': form})
        
        request.session['signup_data'] = {
            'email': email,
            'phone_number': phone_number,
            'password1': form.cleaned_data['password1'],
            'password2': form.cleaned_data['password2'],
        }

        user = User.objects.create_user(username=email, email=email, password=form.cleaned_data['password1'])
        profile = Profile.objects.create(user=user, phone_number=phone_number, email=email)
        
        messages.success(request, 'ثبت نام با موفقیت انجام شد.')
        login(request, user)
        return redirect('product-list')

    return render(request, 'signup.html', {'form': form})


class ForgotPasswordView(View):
    def post(self, request):
        email = request.POST.get('email')
        try:
            profile = Profile.objects.get(email=email)
            profile.generate_otp()
            send_otp_email(profile.email, profile.otp_code)
            messages.success(request, 'کد تایید به ایمیل شما ارسال شد.')
            return redirect('account:verify-otp', user_id=profile.user.id)
        except Profile.DoesNotExist:
            messages.error(request, 'این ایمیل در سیستم ثبت نشده است.')
            return redirect('account:login')

    def get(self, request):
        return render(request, 'forgot_pass.html')
    

class VerifyOTPForPasswordView(View):
    def get(self, request, user_id):
        return render(request, 'verify_otp.html', {'user_id': user_id})

    def post(self, request, user_id):
        otp_code = request.POST.get('otp_code')
        try:
            profile = Profile.objects.get(user_id=user_id)
            if profile.is_otp_valid(otp_code):
                messages.success(request, 'رمز جدید خود را وارد کنید')
                return redirect('account:reset-password', user_id=user_id)
            else:
                messages.error(request, 'کد OTP اشتباه است.')
                return redirect('account:verify-otp', user_id=user_id)
        except Profile.DoesNotExist:
            messages.error(request, 'پروفایل کاربر یافت نشد.')
            return redirect('account:login')
        

class ResetPasswordView(View):
    def get(self, request, user_id):
        return render(request, 'reset_pass.html', {'user_id': user_id})

    def post(self, request, user_id):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'رمزهای عبور وارد شده مطابقت ندارند.')
            return redirect('account:reset-password', user_id=user_id)
        
        try:
            user = User.objects.get(id=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت.')
            login(request, user)
            return redirect('product-list')
        except User.DoesNotExist:
            messages.error(request, 'کاربر یافت نشد.')
            return redirect('account:login')


def VerifyEmailView(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)

    if not request.session.get("otp_sent"):
        profile.generate_otp()
        send_otp_email(profile.email, profile.otp_code)
        messages.success(request, "کد تایید به ایمیل شما ارسال شد.")
        request.session["otp_sent"] = True  
    
    if request.GET.get("resend") == "true":
        profile.resend_otp()
        messages.success(request, "کد تایید جدید به ایمیل شما ارسال شد.")
        return render(request, "verify_email.html", {"profile": profile})

    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        
        if profile.is_otp_valid(otp_entered):
            profile.is_verified = True
            profile.otp_code = None
            profile.otp_expiration = None
            profile.save()
            messages.success(request, "ایمیل شما با موفقیت تأیید شد!")
            return redirect("account:profile-info")  

        messages.error(request, "کد وارد شده نامعتبر است یا منقضی شده است.")

    return render(request, "verify_email.html", {"profile": profile})


class ProfileInfoView(LoginRequiredMixin, View):

    def get(self, request):
        profile = request.user.profile
        form = ProfileInfoForm(instance=profile)
        return render(request, 'profile_info.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = request.user.profile
        form = ProfileInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت به‌روزرسانی شد')
            return redirect('account:profile-info')
        else:
            messages.error(request, 'به‌روزرسانی پروفایل ناموفق بود')
        return render(request, 'profile_info.html', {'form': form, 'profile': profile})


class ProfileOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'profile_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return (
            Order.objects
            .filter(profile=self.request.user.profile)
            .order_by('-date_ordered') 
            .prefetch_related('order_items__product')  
        )


class AddressListView(LoginRequiredMixin, ListView):
    """نمایش لیست آدرس‌ها"""
    template_name = 'profile_address.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(profile=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddressUpdateForm()  
        return context


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressUpdateForm

    def form_valid(self, form):
        address = form.save(commit=False)
        address.profile = self.request.user.profile
        address.save()
        return JsonResponse({'message': 'آدرس با موفقیت اضافه شد.'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressUpdateForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'message': 'آدرس با موفقیت به‌روزرسانی شد.'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    """حذف آدرس موجود"""
    model = Address
    success_url = reverse_lazy('account:address')

    def get_queryset(self):
        return Address.objects.filter(profile=self.request.user.profile)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True}, status=200)
    

class ProfileMagnusPlusView(LoginRequiredMixin, View):

    def get(self, request):
        profile = request.user.profile
        magnusplus_sub = profile.magnusplus_sub
        start_date = profile.magnusplus_start_date
        end_date = profile.get_magnusplus_end_date()

        if magnusplus_sub and end_date:
            remaining_days = (end_date - timezone.now().date()).days
            return render(request, 'profile_magnusplus.html', {'start_date':start_date, 'end_date':end_date, 'magnusplus_sub': magnusplus_sub, 'remaining_days': remaining_days})
        else:
            return render(request, 'profile_magnusplus.html', {})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html', {})