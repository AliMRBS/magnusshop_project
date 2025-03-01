from django import forms
from account.models import Address


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
