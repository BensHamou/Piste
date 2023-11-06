from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import (
    CustomUser,
)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Mot de passe'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Confirmez le mot de passe'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Les mots de passe ne correspondent pas"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.source = 'adminsite'
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Les mots de passe bruts ne sont pas stockés, il n'y a donc aucun moyen de voir le mot de passe "
            "de cet utilisateur, mais vous pouvez modifier le mot de passe en utilisant "
            "<a href=\"{}\">ce formulaire</a>."
        ),
    )
    email = forms.EmailField(label=_("E-mail"), widget=forms.EmailInput)

    class Meta:
        model = CustomUser
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        'id',
        'username',
        'email',
        'last_login',
        'date_joined',
        'source',
    )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Informations personnelles'), {
         'fields': ('first_name', 'last_name', 'bio', 'short_bio', 'profile_picture', 'is_admin')}),
        (_('Autorisations'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display_links = ('id', 'username')
    ordering = ('-id',)
