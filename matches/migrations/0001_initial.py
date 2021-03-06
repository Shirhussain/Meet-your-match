# Generated by Django 3.1.5 on 2021-01-28 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.DecimalField(decimal_places=2, default=0.75, max_digits=5, verbose_name='Percent')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match2', to=settings.AUTH_USER_MODEL, verbose_name='From User')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match', to=settings.AUTH_USER_MODEL, verbose_name='To user')),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
    ]
