from celery import shared_task
import uuid
from datetime import timedelta
from django.utils.timezone import now
from user.models import User, EmailVerification


@shared_task
def send_verification_email(user_id):
    user = User.objects.get(pk=user_id)
    expiration = now() + timedelta(hours=4)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()


