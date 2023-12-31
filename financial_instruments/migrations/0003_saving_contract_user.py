# Generated by Django 4.2.7 on 2023-11-20 05:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial_instruments', '0002_deposit_contract_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='saving',
            name='contract_user',
            field=models.ManyToManyField(related_name='contract_saving', to=settings.AUTH_USER_MODEL),
        ),
    ]
