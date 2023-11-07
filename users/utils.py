from django.conf import settings
from django.core.mail import send_mail

from django.utils.translation import gettext_lazy as _



def send_email(subject, message, to):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to])

def send_activation_code(to, code):
    subject = _('E-mail du code de vérification')
    message = _(f'Votre code de vérification est {code}')
    send_email(subject, message, to)

def send_reset_password_code(to, code):
    subject = 'Code de réinitialisation du mot de passe'
    message = f'Votre code de réinitialisation de mot de passe est {code}'
    send_email(subject, message, to)