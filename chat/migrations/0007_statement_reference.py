# Generated by Django 3.0.2 on 2020-02-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_conversation_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='reference',
            field=models.TextField(blank=True, default=''),
        ),
    ]
