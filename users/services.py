from django.core.mail import send_mail

from config import settings


def send_new_password(email, new_password):
    send_mail(
        subject='Вы сменили пароль',
        massage=f'Ваш новый пароль:{new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
    