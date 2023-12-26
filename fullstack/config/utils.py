from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import Http404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404

from six import text_type

import threading

from account.models import User


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


def decode_user(uidb64, token):
    id = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=id)
    print(account_activation_token.check_token(user, token))

    if not account_activation_token.check_token(user, token):
        raise Http404
    return user


class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def send_email(recipient_email, email_subject, text_content):
    email = EmailMultiAlternatives(
        email_subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [recipient_email],
    )
    EmailThread(email).start()
