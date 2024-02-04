from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.shortcuts import (
    redirect,
    render,
)
from django.contrib.auth.decorators import login_required

from .forms import (
    CustomLoginForm,
    RegisterForm,
    ForgetPasswordEmailCodeForm,
    ChangePasswordForm,
    OtpForm,
)
from .models import OtpCode, CustomUser
from .utils import (
    send_activation_code,
    send_reset_password_code,
)
from .decorators import only_authenticated_user, redirect_authenticated_user
import requests
import json
import uuid
from django.urls import reverse

@only_authenticated_user
def home_view(request):
    return render(request, 'users/home.html')

@login_required(login_url='login')
def refreshUsersList(request):
    
    usernames = CustomUser.objects.values_list('username', flat=True)
    
    API_Users = 'https://api.ldap.groupe-hasnaoui.com/get/users?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJUb2tlbiI6IkZvciBEU0kiLCJVc2VybmFtZSI6ImFjaG91cl9hciJ9.aMy1LUzKa6StDvQUX54pIvmjRwu85Fd88o-ldQhyWnE'
    GROUP_Users = 'https://api.ldap.groupe-hasnaoui.com/get/users/group/GSH-PST?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJUb2tlbiI6IkZvciBEU0kiLCJVc2VybmFtZSI6ImFjaG91cl9hciJ9.aMy1LUzKa6StDvQUX54pIvmjRwu85Fd88o-ldQhyWnE'

    response = requests.get(API_Users)
    response_ = requests.get(GROUP_Users)

    if response.status_code == 200 and response_.status_code == 200:
        data = json.loads(response.content)
        group_users = json.loads(response_.content)['members']

        new_users_list = [user for user in data['users'] if user['fullname'] in group_users and user['AD2000'] not in usernames]

        for user in new_users_list:
            user = CustomUser(username= user['AD2000'], password='password', is_admin=False, first_name= user['fname'], email= user['mail'].lower(), last_name = user['lname'])
            user.save()
    else:
        print('Error: could not fetch data from API')

    cache_param = str(uuid.uuid4())
    url_path = reverse('users:home')
    redirect_url = f'{url_path}?cache={cache_param}'

    return redirect(redirect_url)


@redirect_authenticated_user
def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username_or_email'], password=form.cleaned_data['password'])
            if user:
                if not user.is_active:
                    messages.warning(request, _(
                        f"Il semblerait que vous n'ayez pas encore vérifié votre adresse e-mail - {user.email}"))
                    return redirect('users:activate_email')
                else:
                    login(request, user)
                    return redirect('users:home')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})


@only_authenticated_user
@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@redirect_authenticated_user
def registeration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.source = 'Register'
            user.save(True)

            code = get_random_string(20)
            otp = OtpCode(code=code, user=user)
            otp.save(True)
            try:
                send_activation_code(user.email, code)
            except:
                otp.delete()
                user.delete()
                messages.error(request, _('Échec lors de l\'envoi du code !'))
            else:
                messages.success(
                    request, _(f'Nous avons envoyé un code de vérification à votre adresse e-mail- {user.email}'))
                return redirect('users:activate_email')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@redirect_authenticated_user
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordEmailCodeForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            user = get_user_model().objects.get(**username_or_email)
            code = get_random_string(20)

            otp = OtpCode(code=code, user=user, email=user.email)
            otp.save()

            try:
                send_reset_password_code(user.email, code)
            except:
                otp.delete()
                messages.error(request, _('Failed while sending code!'))
            else:
                messages.success(request, _(
                    f"Nous avons envoyé un OTP de réinitialisation de mot de passe à votre adresse e-mail {user.email}"))
                return redirect('users:reset_code')
    else:
        form = ForgetPasswordEmailCodeForm()
    return render(request, 'users/forgot_password.html', context={'form': form})

@redirect_authenticated_user
def check_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            user = otp.user
            otp.delete() 
            user.is_active = True
            user.save()
            return redirect('users:login')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})

@redirect_authenticated_user
def check_reset_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            request.session['email'] = otp.user.email
            messages.success(request, _(
                "Veuillez créer un nouveau mot de passe que vous n'utilisez sur aucun autre site."))
            return redirect('users:reset_new_password')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})


@redirect_authenticated_user
def reset_new_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            email = request.session['email']
            del request.session['email']
            user = CustomUser.objects.get(email=email)
            user.password = make_password(form.cleaned_data["new_password2"])
            user.save()
            messages.success(request, _(
                "Votre mot de passe a changé. Vous pouvez maintenant vous connecter avec votre nouveau mot de passe."))
            return redirect('users:login')
    else:
        form = ChangePasswordForm()
    return render(request, 'users/new_password.html', {'form': form})
