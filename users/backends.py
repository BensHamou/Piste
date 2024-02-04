from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from requests.auth import HTTPBasicAuth
import requests
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib import messages 
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            if username in ['admin', 'admin@admin.com']:
                if check_password(password, user.password):
                    return user
                else:
                    messages.error(request, "Mot de passe incorrect.")
                    return None
            
            auth = HTTPBasicAuth(user.email, password)

            response = requests.post('https://api.ldap.groupe-hasnaoui.com/gshpst/auth', auth=auth)

            if not response.status_code == 200:
                messages.error(request, "Problème avec la connexion au serveur.")
            else:
                if not response.json().get('authenticated'):
                    messages.error(request, "Mot de passe incorrect.")
                else:
                    return user
        except CustomUser.DoesNotExist:
            messages.error(request, "Utilisateur pas trouvé.")
        return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
