from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Contact, Profile


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already in use.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") and cleaned.get("password2") and cleaned["password1"] != cleaned["password2"]:
            self.add_error("password2", "Passwords do not match.")
        return cleaned


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "message")

    def clean_message(self):
        return self.cleaned_data["message"].strip()


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image",)

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Image must be 5 MB or smaller.")
        if getattr(image, "content_type", "") not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValidationError("Upload a JPEG, PNG, or WebP image.")
        return image
