# Generated by Django 3.1.5 on 2021-02-03 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matches', '0004_jobmatch_show'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('read_at', models.DateField(blank=True, null=True, verbose_name='Reat at')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_user', to=settings.AUTH_USER_MODEL, verbose_name='Match User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_user', to=settings.AUTH_USER_MODEL, verbose_name='Main User')),
            ],
            options={
                'verbose_name': 'MatchList',
                'verbose_name_plural': 'MatchLists',
                'ordering': ['-updated', '-timestamp'],
            },
        ),
    ]
