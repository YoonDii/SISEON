

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unname', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Free',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', mdeditor.fields.MDTextField()),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('like_free', models.ManyToManyField(related_name='like_free', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReComment1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200, verbose_name='답글')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_comment_user', to='free.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('free', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='free.free')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='free',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_user', to='free.free'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_com_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
