from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import threading
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def send_email(request, user, title, content):
    current_site = get_current_site(request)
    email_body = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }
    
    link = reverse('activate', kwargs={
                    'uidb64': email_body['uid'], 'token': email_body['token']})
    
    email_body.update({'url': 'http://'+current_site.domain+link})
    
    email_subject = title
    html_content = content
    text_content = content
    
    email = EmailMultiAlternatives(
        email_subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.attach_alternative(html_content, "text/html")
    EmailThread(email).start()