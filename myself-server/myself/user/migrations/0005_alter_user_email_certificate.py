# Generated by Django 4.2 on 2023-05-26 21:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_recipient', models.CharField(max_length=255, verbose_name='Имя получателя')),
                ('phone_number_recipient', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='Не корректный номер телефона', regex='^((8|\\+374|\\+994|\\+995|\\+375|\\+7|\\+380|\\+38|\\+996|\\+998|\\+993)[\\- ]?)?\\(?\\d{3,5}\\)?[\\- ]?\\d{1}[\\- ]?\\d{1}[\\- ]?\\d{1}[\\- ]?\\d{1}[\\- ]?\\d{1}(([\\- ]?\\d{1})?[\\- ]?\\d{1})?$')])),
                ('email_recipient', models.EmailField(blank=True, max_length=254)),
                ('value', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Сумма')),
                ('congratulation', models.TextField(default='Поздравляю!!!')),
                ('name_payer', models.CharField(max_length=255, verbose_name='Имя отправителя')),
                ('phone_number_payer', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='Не корректный номер телефона', regex='^((8|\\+374|\\+994|\\+995|\\+375|\\+7|\\+380|\\+38|\\+996|\\+998|\\+993)[\\- ]?)?\\(?\\d{3,5}\\)?[\\- ]?\\d{1}[\\- ]?\\d{1}[\\- ]?\\d{1}[\\- ]?\\d{1}[\\- ]?\\d{1}(([\\- ]?\\d{1})?[\\- ]?\\d{1})?$')], verbose_name='Номер отправителя')),
                ('email_payer', models.EmailField(blank=True, max_length=254)),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
            },
        ),
    ]