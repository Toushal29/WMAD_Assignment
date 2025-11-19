from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Customer

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

        # Placeholders
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

        # Remove Django’s strong password hints
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

        # Default role (hidden)
        # signup page must always create customer
        self.role = "customer"

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.phone_no = self.cleaned_data['phone_no']
        user.role = "customer"       # FIXED: role always customer on signup

        if commit:
            user.save()

            # Create customer profile
            Customer.objects.create(
                user=user,
                address=self.cleaned_data['address']
            )

        return user
