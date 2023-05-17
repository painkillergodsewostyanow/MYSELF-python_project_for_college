from django.db import models
from django.core.validators import RegexValidator


class Certificate(models.Model):
    phone_regex = RegexValidator(regex=r'^((8|\+374|\+994|\+995|\+375|\+7|\+380|\+38|\+996|\+998|\+993)'
                                       r'[\- ]?)?\(?\d{3,5}\)?[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}[\- ]?\d{1}'
                                       r'(([\- ]?\d{1})?[\- ]?\d{1})?$', message="Не корректный номер телефона")

    name_recipient = models.CharField(max_length=255)
    phone_number_recipient = models.CharField(validators=[phone_regex], max_length=17)
    email_recipient = models.EmailField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    congratulation = models.TextField(default="Поздравляю!!!")
    name_payer = models.CharField(max_length=255)
    phone_number_payer = models.CharField(validators=[phone_regex], max_length=17)
    email_payer = models.EmailField(blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Сертификат номер {self.pk} для {self.name_recipient}"

    class Meta:
        verbose_name = "Сертификаты"
        verbose_name_plural = "Сертификаты"

