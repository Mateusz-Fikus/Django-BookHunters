# Generated by Django 3.1.6 on 2021-03-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0014_pending_id_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='pending',
            name='message',
            field=models.CharField(blank=True, default=None, max_length=250),
        ),
    ]
