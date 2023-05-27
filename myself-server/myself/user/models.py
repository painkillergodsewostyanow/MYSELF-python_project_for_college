from django.core.validators import RegexValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
from store.models import Product


class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to="users_img", null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


class Certificate(models.Model):
    phone_regex = RegexValidator(regex=r'^((8|\+374|\+994|\+995|\+375|\+7|\+380|\+38|\+996|\+998|\+993)'
                                       r'[\- ]?)?\(?\d{3,5}\)?[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}'
                                       r'(([\- ]?\d{1})?[\- ]?\d{1})?$', message="Не корректный номер телефона")

    user = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True)
    name_recipient = models.CharField(max_length=255, verbose_name="Имя получателя")
    phone_number_recipient = models.CharField(validators=[phone_regex], max_length=17)
    email_recipient = models.EmailField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Сумма")
    congratulation = models.TextField(default="Поздравляю!!!")
    name_payer = models.CharField(max_length=255, verbose_name="Имя отправителя")
    phone_number_payer = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Номер отправителя")
    email_payer = models.EmailField(blank=True)
    is_used = models.BooleanField(default=False)

    def send_notify_email(self, code=settings.USER_GET_CERTIFICATE):
        subject = f"MYSELF: сертификат от {self.email_payer}"
        message = f"На ваш адресс электронной почты был куплен сертификат \n" \
                  f"на сумму: {self.value} \n" \
                  f"почта дарителя{self.email_payer} номер дарителя: {self.phone_number_payer}\n" \
                  f"текст поздравления: {self.congratulation}\n" \
                  f"так как у вас уже создан аккаунт, с подтвержденной почтой, сертификат добавлен на него"

        if code == settings.USER_NOT_CREATED:
            message = f"На ваш адресс электронной почты был куплен сертификат \n" \
                      f"на сумму: {self.value} \n" \
                      f"почта дарителя: {self.email_payer} номер дарителя: {self.phone_number_payer}\n" \
                      f"текст поздравления: {self.congratulation}\n" \
                      f"что бы воспользоваться сертификатом, зарегистрируйте аккаунт и подтвердите почту\n" \
                      f"{settings.DOMAIN_NAME}{reverse('user:reg')}"

        if code == settings.USER_EMAIL_NOT_VERIFIED:
            message = f"На ваш адресс электронной почты был куплен сертификат \n" \
                      f"\tна сумму: {self.value} \n" \
                      f"\tпочта дарителя{self.email_payer} номер дарителя: {self.phone_number_payer}\n" \
                      f"текст поздравления: {self.congratulation}\n" \
                      f"что бы воспользоваться сертификатом, подтвердите почту\n" \
                      f"{settings.DOMAIN_NAME}{reverse('store:home')}"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.email_recipient],
            fail_silently=False,
        )

    def __str__(self):
        return f"Сертификат номер {self.pk} для {self.name_recipient}"

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verification_email(self, is_expired=False):
        link = f"{settings.DOMAIN_NAME}" \
               f"{reverse('user:email_verification', kwargs={'email': self.user.email, 'code': self.code})}"
        subject = f'Myself запрос на подтверждение учетной записи для {self.user.username}'
        message = f'Перейдите по ссылке что бы подтвердить учетную запись: {link}'

        if is_expired:
            message = f'Старая ссылка для подтверждения почты устарела, новая ссылка: {link}'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration


class Favorite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Избранное для {self.user.username}"
