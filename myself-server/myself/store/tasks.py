from celery import shared_task
from user.models import User, Certificate
from django.conf import settings


@shared_task
def send_notify_email(certificate_id):
    certificate = Certificate.objects.get(pk=certificate_id)
    user = User.objects.filter(email=certificate.email_recipient).last()

    if not user:
        certificate.send_notify_email(code=settings.USER_NOT_CREATED)
        return

    if not user.is_email_verified:
        certificate.send_notify_email(code=settings.USER_EMAIL_NOT_VERIFIED)
        return
    else:
        certificate.user = user
        certificate.save()
        certificate.send_notify_email()
