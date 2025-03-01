from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from magnusplus.models import Package
from django.utils import timezone
from django.urls import reverse

class PricingView(View):
    def get_context_data(self):
        packages = Package.objects.filter(is_enable=True)
        return dict(packages=packages)

    def get(self, request, *args, **kwargs):
        return render(request, 'pricing.html', self.get_context_data())


class PurchaseSubscriptionView(View):  
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('account:login') 
            next_url = reverse('magnusplus:pricing')  
            return redirect(f"{login_url}?next={next_url}")

        package_id = request.POST.get('package_id')

        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            messages.error(request, 'پکیج مورد نظر یافت نشد.')
            return redirect('product-list')

        profile = request.user.profile
        if profile.magnusplus_sub:
            messages.warning(request, 'شما قبلاً یک اشتراک خریداری کرده‌اید.')
            return redirect('magnusplus:pricing')

        profile.magnusplus_sub = package
        profile.magnusplus_start_date = timezone.now().date()
        profile.save()

        messages.success(request, f'اشتراک {package.title} با موفقیت خریداری شد.')
        return redirect('product-list')
