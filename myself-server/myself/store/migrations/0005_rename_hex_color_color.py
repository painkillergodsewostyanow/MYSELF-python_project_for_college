# Generated by Django 4.2 on 2023-06-04 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_color_product_product_color_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='hex',
            new_name='color',
        ),
    ]