# Generated by Django 3.2.13 on 2022-12-04 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='check',
            field=models.BooleanField(default=False),
        ),
    ]
