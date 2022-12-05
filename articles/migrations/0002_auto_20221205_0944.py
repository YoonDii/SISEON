# Generated by Django 3.2.13 on 2022-12-05 00:44

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
        migrations.AlterField(
            model_name='articles',
            name='category',
            field=models.CharField(choices=[('질문유형을 선택해 주세요.', '질문유형을 선택해 주세요.'), ('CS', 'CS'), ('알고리즘', '알고리즘'), ('진로', '진로'), ('오류', '오류'), ('기타', '기타')], default='질문유형을 선택해 주세요.', max_length=50),
        ),
    ]