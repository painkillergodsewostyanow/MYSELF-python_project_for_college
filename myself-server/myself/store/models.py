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
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    SEX = [
        (1, "Мужской"),
        (2, "Женский"),
        (3, "Унисекс")
    ]
    image = models.ImageField(upload_to="products_img")
    title = models.CharField(max_length=255)
    description = models.TextField()
    colors = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    sex = models.PositiveSmallIntegerField("Пол", choices=SEX)

    def __str__(self):
        return f"{self.title}, {self.colors}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"



