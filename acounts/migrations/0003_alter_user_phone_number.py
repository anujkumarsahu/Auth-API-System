# Generated by Django 5.2 on 2025-04-16 02:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0002_user_phone_number_alter_user_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Phone number must be exactly 10 digits.')], verbose_name='phone number'),
        ),
    ]
