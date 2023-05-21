# Generated by Django 4.2 on 2023-05-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'Размеры', 'verbose_name_plural': 'Размеры'},
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='description',
        ),
    ]