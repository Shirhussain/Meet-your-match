# Generated by Django 3.1.5 on 2021-01-24 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Profiles/', verbose_name='Image')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timstamp')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'UserPicture',
                'verbose_name_plural': 'UserPictures',
            },
        ),
    ]
