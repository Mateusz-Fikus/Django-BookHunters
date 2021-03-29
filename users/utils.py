#GENERATOR TOKENÓW DO POTWIERDZANIA MAILA
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

#DO MAILA
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

#TOKENY WERYFIKACJI KONTA MAILEM
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.urls import reverse

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) + text_type(user.username) )

token_generator = AppTokenGenerator()


def email(task, **kwargi):
    domain = kwargi["domain"]
    user = kwargi["user"]

    if task == "REG" or task == "RES":
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        if task == "REG":
            link = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': token_generator.make_token(user)
                })
            subject = 'Welcome to BookHunters!'
            message = 'Hey ' + user.username + ' Please verify your account by clicking this link\n'

        if task == "RES":
            link = reverse('reset_password', kwargs={
                'uidb64': uidb64, 'token': token_generator.make_token(user)
                })
            subject = 'Password reset'
            message = 'Hey ' + user.username + ' Visit this link to change your password\n'

    if task == "NOT":
        offer = kwargi['offer']            
        link = reverse('offer_info', kwargs={
            'id': offer.id
        })
        subject = 'Your book request has been accepted!'
        message = 'Your purchase request for ' + offer.title + ' has been accepted!\n'

    url = domain + link
    message += url
    recipient = str(user.email)
    send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)


