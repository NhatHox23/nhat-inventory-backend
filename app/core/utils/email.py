from django.core.mail import EmailMessage

from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User


def send_mail(data):
    email = EmailMessage(subject=data['subject'], body=data[
        'email_body'], to=data['to_email'])
    email.send()


def get_token(user_id):
    """Helper function to get access token"""
    user = User.objects.get(id=user_id)
    return RefreshToken.for_user(user)


def concat_link(*args, token=None):
    """Helper to concat"""
    link = "http://"
    for i in args:
        link += i
    if token:
        link += "?token=" + str(token)
    return link
