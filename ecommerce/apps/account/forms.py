from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import Address, UserBase


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "address_line",
            "address_line2",
            "town_city",
            "postcode",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Full Name",
            }
        )
        self.fields["phone"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Phone",
            }
        )
        self.fields["address_line"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Address",
            }
        )
        self.fields["address_line2"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Second address",
            }
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "City"}
        )
        self.fields["postcode"].widget.attrs.update(
            {
                "class": "form-control mb-2 account-form",
                "placeholder": "Postcode",
            }
        )


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Username", min_length=4, max_length=50, help_text="Required"
    )
    email = forms.EmailField(
        label="Email",
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput
    )

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "email",
        )

    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()
        check_name = UserBase.objects.filter(user_name=user_name)
        if check_name.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        check_password = self.cleaned_data
        if check_password["password"] != check_password["password2"]:
            raise forms.ValidationError("Password do not match")
        return check_password["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Use another Email, thatis already taken"
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat Password"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pw",
            }
        )
    )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "form-email",
                "readonly": "readonly",
            }
        ),
    )
    # user_name = forms.CharField(
    #     label='Username', min_length=4, widget=forms.TextInput(
    #         attrs={'class': 'form-control mb-3',
    #                'placeholder': 'Username',
    #                'id': 'form-username',
    #                'readonly': 'readonly'}))
    first_name = forms.CharField(
        label="Firstname",
        min_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Firstname",
                "id": "form-firstname",
            }
        ),
    )

    class Meta:
        model = UserBase
        fields = (
            "email",
            "first_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placegolder": "Email",
                "id": "form-email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = UserBase.objects.filter(email=email)
        if not user:
            raise forms.ValidationError("We can not find that email")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "New password",
                "id": "form-newpass",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Repeat password",
                "id": "form-newpass2",
            }
        ),
    )
