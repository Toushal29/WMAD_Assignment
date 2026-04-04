# C:\Users\...\WMAD_Assignment\WMAD_project\web_app\forms.py

# this file defines the forms used in the web application, including a custom user creation form that extends Django's built-in UserCreationForm to include additional fields like email, phone, and address, as well as a profile update form for users to update their information, and a review form for submitting reviews with ratings and comments. The forms also include custom initialization and save methods to handle specific logic related to user profiles and reviews.

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Customer, Review


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "address",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone": "Phone Number",
            "address": "Address",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for field, placeholder in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs.update({"placeholder": placeholder})

        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"],
            )

        return user


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(required=False)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["readonly"] = True
        self.fields["username"].widget.attrs["class"] = "form-control-plaintext"

        if user:
            self.fields["username"].initial = user.username
            profile = Customer.objects.filter(user=user).first()
            if profile:
                self.fields["phone"].initial = profile.phone
                self.fields["address"].initial = profile.address

    def clean_username(self):
        return self.instance.username

    def save(self, commit=True):
        user = super().save(commit=commit)
        Customer.objects.update_or_create(
            user=user,
            defaults={
                "phone": self.cleaned_data["phone"],
                "address": self.cleaned_data["address"],
            },
        )
        return user


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Write your review...",
            }
        ),
        max_length=500,
        required=False,
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }

    def clean_comment(self):
        return self.cleaned_data.get("comment", "").strip()
