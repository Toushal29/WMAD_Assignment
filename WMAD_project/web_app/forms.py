# C:\Users\toush\Desktop\WMAD_Assignment\WMAD_project\web_app\forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Customer

#SIGNUP FORM
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "required": True,
            "placeholder": "Email",
            "pattern": r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        })
    )

    phone_no = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            "required": True,
            "placeholder": "Phone Number",
            "pattern": r"^[0-9]{7,15}$",
            "title": "Phone number must be 7-15 digits."
        })
    )

    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Address",
            "maxlength": "255"
        })
    )

    class Meta:
        model = Users
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone_no', 'address',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        html5_rules = {
            'username': {
                "required": True,
                "minlength": "3",
                "maxlength": "20",
                "pattern": r"^[A-Za-z0-9_]{3,20}$",
                "title": "Only letters, numbers, and underscores allowed (3–20 chars).",
                "placeholder": "Username"
            },
            'first_name': {
                "required": True,
                "minlength": "2",
                "maxlength": "30",
                "pattern": r"^[A-Za-z\- ]+$",
                "title": "Only letters, hyphens and spaces.",
                "placeholder": "First Name"
            },
            'last_name': {
                "required": True,
                "minlength": "2",
                "maxlength": "30",
                "pattern": r"^[A-Za-z\- ]+$",
                "title": "Only letters, hyphens and spaces.",
                "placeholder": "Last Name"
            },
            'password1': {
                "required": True,
                "minlength": "8",
                "placeholder": "Password",
                "title": "At least 8 characters."
            },
            'password2': {
                "required": True,
                "minlength": "8",
                "placeholder": "Confirm Password",
                "title": "Repeat same password."
            }
        }

        for field, attrs in html5_rules.items():
            if field in self.fields:
                self.fields[field].widget.attrs.update(attrs)

        #remove django's default password help text
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_no = self.cleaned_data['phone_no']
        user.role = "customer"

        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                address=self.cleaned_data.get('address', "")
            )
        return user


#PROFILE UPDATE FORM
class ProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            "maxlength": "255",
            "placeholder": "Address"
        })
    )

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'phone_no']

        widgets = {
            "email": forms.EmailInput(attrs={
                "required": True,
                "pattern": r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
            }),
            "phone_no": forms.TextInput(attrs={
                "required": True,
                "pattern": r"^[0-9]{7,15}$",
                "title": "Phone number must be 7-15 digits."
            }),
            "first_name": forms.TextInput(attrs={
                "required": True,
                "minlength": "2",
                "maxlength": "30",
                "pattern": r"^[A-Za-z\- ]+$",
            }),
            "last_name": forms.TextInput(attrs={
                "required": True,
                "minlength": "2",
                "maxlength": "30",
                "pattern": r"^[A-Za-z\- ]+$",
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            try:
                self.fields['address'].initial = user.customer.address
            except Customer.DoesNotExist:
                self.fields['address'].initial = ""

    def save(self, commit=True):
        user = super().save(commit)
        address = self.cleaned_data.get("address", "")
        Customer.objects.update_or_create(
            user=user,
            defaults={'address': address}
        )
        return user
