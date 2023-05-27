# Generated by Django 4.2 on 2023-05-26 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_email_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='certificate',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='user.certificate'),
        ),
    ]
