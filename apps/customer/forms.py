from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import (
    User, UserProfile
)


class UserCreationAdminForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreationAdminForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email', 'required': True,
             'class': 'form-control'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password',
             'required': True, 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat Password',
             'required': True, 'class': 'form-control'})
        if self.instance.id:
            self.fields['email'].widget.attrs.update({'readonly': True})
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = _("Passwords don't match")
            self.add_error('password1', msg)
            self.add_error('password2', msg)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationAdminForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeAdminForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"), help_text=_(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.CharField(label=_('Email Address'), max_length=255)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email', 'autocomplete': 'off',
             'required': True})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Password', 'autocomplete': 'off',
             'required': True})

    def clean(self):
        email = self.cleaned_data.get('email', '')
        password = self.cleaned_data.get('password', '')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.HiddenInput(), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email', 'required': True,
             'class': 'form-control'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password', 'class': 'form-control',
             'onfocus': "if(this.getAttribute('type')==='text') "
                        "this.setAttribute('type','password'); "
                        "this.setAttribute('value','')"
             })
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat Password', 'class': 'form-control',
             'onfocus': "if(this.getAttribute('type')==='text')"
                        " this.setAttribute('type','password'); "
                        "this.setAttribute('value','')"
             })
        self.fields['first_name'].widget.attrs.update(
            {'placeholder': 'First Name', 'class': 'form-control'})
        self.fields['team'].widget.attrs.update(
            {'placeholder': 'Team', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update(
            {'placeholder': 'Last Name', 'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update(
            {'placeholder': 'is active', 'class': 'styled'})
        self.fields['is_admin'].widget.attrs.update(
            {'placeholder': 'is admin', 'class': 'styled'})

        if self.instance.id:
            self.fields['email'].widget.attrs.update({'readonly': True})
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    class Meta:
        model = User
        fields = "__all__"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                msg = _("Passwords don't match")
                self.add_error('password1', msg)
                self.add_error('password2', msg)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update(
            {'placeholder': 'address', 'class': 'form-control'})
        self.fields['document_type'].widget.attrs.update(
            {'placeholder': 'document_type', 'required': True,
             'class': 'form-control'})
        self.fields['document_number'].widget.attrs.update(
            {'placeholder': 'document_number', 'required': True,
             'class': 'form-control'})
        self.fields['home_phone'].widget.attrs.update(
            {'placeholder': 'home_phone', 'class': 'form-control'})
        self.fields['mobile_phone'].widget.attrs.update(
            {'placeholder': 'mobile_phone', 'class': 'form-control'})
        self.fields['logo_profile'].widget.attrs.update(
            {'placeholder': 'image', 'class': 'file-styled'})

    class Meta:
        model = UserProfile
        fields = ["address", "document_type", "document_number", "home_phone",
                  "mobile_phone", "logo_profile"]

    def save(self, user=None, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        if user:
            profile.user = user
        profile.save()
        return profile
