from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, redirect
from django.conf import settings
from django.db import transaction

class DateInput(forms.DateInput):
    input_type = "date"

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label="Re-enter password", widget=forms.PasswordInput, )
    password = forms.CharField(widget=forms.PasswordInput,  help_text="must be more than 6 characters")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    def clean_password2(self, *args, **kwargs):
        data = self.cleaned_data
        p = data["password2"]
        p_1 = data["password"]
        if len(p) < 6:
            raise forms.ValidationError("Your password should be 6 or more characters")
        if p == p_1:
            return p
        raise forms.ValidationError("Your passwords do not match")

class ProfileForm(forms.ModelForm): 
    dob = forms.DateField(
        widget=DateInput,
        label="Date of Birth",
    )
    image = forms.FileField(
        label="Passport Picture",
    )
    class Meta:
        model = models.Profile
        fields = ("phone_number","image","digital_address","sex","dob","next_of_kin","next_of_kin_phone_number",
                    "next_of_kin_digital_address", "account_type", "account_balance", "id_type", "id_number",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

class DepositeForm(forms.ModelForm):
    class Meta:
        model = models.Deposite
        fields = ("amount",)

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = models.Withdrawal
        fields = ("amount",)