from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from requests.auth import HTTPBasicAuth
import requests
from .models import CustomUser
from django.contrib.auth.hashers import check_password


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        if username == 'admin':
            user = CustomUser.objects.get(username = 'admin')
            if check_password(password, user.password):
                return user
        
        auth = HTTPBasicAuth(username, password)

        response = requests.post('https://api.ldap.groupe-hasnaoui.com/gshpst/auth', auth=auth)

        if response.status_code == 200 and response.json().get('authenticated'):
            user = CustomUser.objects.get(username = response.json().get('userinfo')['ad2000'])
            return user
        return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
