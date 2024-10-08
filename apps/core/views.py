import json
import os
import string
import random
import requests
import binascii

from hashlib import sha256
from decouple import config
from datetime import datetime
from dataclasses import dataclass
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import AccessToken
from django_rest_passwordreset.signals import reset_password_token_created

from apps.user.models import User


EMAIL_URL = config('EMAIL_URL')
EMAIL_FROM = config('EMAIL_FROM')
EMAIL_TOKEN = config('EMAIL_TOKEN')
EMAIL_TEMPLATE_RESET_PASSWORD = config('EMAIL_TEMPLATE_RESET_PASSWORD')


def validate_password(pswrd: str):
    if len(pswrd) < 8:
        return False
    if not any([char in pswrd for char in string.ascii_uppercase]):
        return False
    if not any([symbol in pswrd for symbol in string.punctuation]):
        return False
    return pswrd


def generate_random_password():
    characters = list(string.ascii_letters + string.digits)
    sp_char = list("!@#$%^&*()")
    length = 10
    random.shuffle(characters+sp_char)
    da_password = []
    for i in range(length):
        da_password.append(random.choice(characters+sp_char))
    random.shuffle(da_password)
    return "".join(da_password)


def hashfy(data=None):
    if not data:
        new_hash = sha256(str(datetime.timestamp(datetime.now())).encode()).hexdigest()
    else:
        data['timestamp'] = str(datetime.timestamp(datetime.now()))
        new_hash = sha256(str(data).encode()).hexdigest()
    return new_hash


def read_token(access_token):
    token_obj = AccessToken(access_token)
    user_id = token_obj['user_id']
    user = User.objects.get(id=user_id)
    content = {'user_id': user_id, 'user': user}
    return content


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    MailSending(
        subject="Recuperação de senha",
        from_email=EMAIL_FROM,
        recipient_list=[reset_password_token.user.email],
        template_id=EMAIL_TEMPLATE_RESET_PASSWORD,
        context_template={
            "%name%": reset_password_token.user.first_name,
            "%token%": str(reset_password_token.key)
        },
    ).send_email()


@dataclass
class MailSending:
    subject: str
    from_email: str
    recipient_list: list
    template_id: str
    context_template: dict

    def get_payload(self):
        data = {
            'subject': self.subject,
            'from_email': self.from_email,
            'recipient_list': self.recipient_list,
            'template_id': self.template_id,
            'context_template': self.context_template
        }

        boundary = binascii.hexlify(os.urandom(16)).decode('ascii')

        payload = (
                ''.join(
                    '--%s\r\n'
                    'Content-Disposition: form-data; name=data\r\n'
                    '\r\n'
                    '%s\r\n' % (boundary, json.dumps(data))
                ) + '--%s--\r\n' % boundary
        )

        content_type = "multipart/form-data; boundary=%s" % boundary

        return {
            'payload': payload,
            'headers': {
                'Content-Type': content_type,
                'Authorization': F"Bearer {EMAIL_TOKEN}"
            }
        }

    def send_email(self):
        params = self.get_payload()

        response = requests.request("POST", EMAIL_URL, data=params["payload"], headers=params["headers"])

        print(response.text)

