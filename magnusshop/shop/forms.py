from django import forms
from .models import ProductComment

class ProductCommentForm(forms.ModelForm):
    name = forms.CharField(
        label="نام",
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'نام'
        })
    )
    comment = forms.CharField(
        label="کامنت",
        required=True,
        max_length=600,
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 border border-1 border-gray-300 placeholder:text-gray-400 focus:border-2 focus:border-indigo-600 sm:text-sm/6',
            'placeholder': 'کامنت'
        })
    )
   
    class Meta:
        model = ProductComment
        fields = ['name', 'comment']


