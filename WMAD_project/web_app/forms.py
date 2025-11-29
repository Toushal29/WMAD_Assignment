# C:\Users\toush\Desktop\WMAD_Assignment\WMAD_project\web_app\forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Customer

# SIGNUP FORM
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Users
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone_no', 'address',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_no': 'Phone Number',
            'address': 'Address',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

        for field, placeholder in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs.update({
                    'placeholder': placeholder
                })

        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_no = self.cleaned_data['phone_no']
        user.role = "customer"     # role always customer for this form

        # Create Customer profile
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                address=self.cleaned_data.get('address', "")
            )
        return user

# PROFILE UPDATE FORM
class ProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'phone_no']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Load user's current address
        if user:
            try:
                self.fields['address'].initial = user.customer.address
            except Customer.DoesNotExist:
                self.fields['address'].initial = ""

    # Update customer.address
    def save(self, commit=True):
        user = super().save(commit)
        address = self.cleaned_data.get("address", "")
        Customer.objects.update_or_create(
            user=user,
            defaults={'address': address}
        )
        return user