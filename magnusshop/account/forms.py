from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from account.models import Profile, Address



class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=11,
        min_length=11,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='شماره موبایل باید ۱۱ رقم و فقط شامل اعداد باشد.'
            ),
        ],
        error_messages={
            'required': 'وارد کردن شماره موبایل الزامی است.',
            'max_length': 'شماره موبایل نمی‌تواند بیش از ۱۱ رقم باشد.',
            'min_length': 'شماره موبایل نمی‌تواند کمتر از ۱۱ رقم باشد.',
        },
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': '09123456789',
            'style': 'direction: rtl; max-width: 100%;'
        })
    )

    email = forms.EmailField(
        label='ایمیل',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'example@gmail.com',
            'style': 'direction: rtl; max-width: 100%;',
        })
    )

    password1 = forms.CharField(
        label='رمز عبور',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'حداقل 8 کاراکتر و ترکیب حروف و اعداد',
            'style': 'direction: rtl; max-width: 100%;'
        })
    )

    password2 = forms.CharField(
        label='تکرار رمز عبور',
        required=True,
        error_messages={
            'required': 'تکرار رمز عبور الزامی است.',
        },
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'رمز عبور را دوباره وارد کنید',
            'style': 'direction: rtl; max-width: 100%;'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(profile__phone_number=phone_number).exists():
            raise ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
            profile.save()
        return user


class ProfileInfoForm(forms.ModelForm):

    first_name = forms.CharField(
        label="نام",
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'نام خود را وارد کنید',
            'style': 'width: 30%;'
        })
    )

    last_name = forms.CharField(
        label="نام خانوادگی",
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
            'style': 'width: 30%;'

        })
    )

    email = forms.EmailField(
        required=False,
        label="ایمیل",
        widget=forms.EmailInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'example@email.com',
            'style': 'width: 30%;'

        })
    )

    phone_number = forms.CharField(
        required=True,
        label='تلفن همراه',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder':'شماره تلفن',
            'style': 'width: 30%;'

            }),
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number']



class AddressUpdateForm(forms.ModelForm):
    
    province = forms.CharField(
        label="استان",
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'استان'
        })
    )
    city = forms.CharField(
        label="شهر",
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'شهر'
        })
    )
    address = forms.CharField(
        label="آدرس",
        required=True,
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'آدرس'
        })
    )
    house_number = forms.CharField(
        label="پلاک",
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'پلاک'
        })
    )
    unit_number = forms.CharField(
        label="واحد",
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'واحد'
        })
    )
    zipcode = forms.CharField(
        label="کدپستی",
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'کدپستی'
        })
    )

    class Meta:
        model = Address
        fields = ['province', 'city', 'address', 'house_number', 'unit_number', 'zipcode']
