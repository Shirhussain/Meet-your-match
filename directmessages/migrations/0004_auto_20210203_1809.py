# Generated by Django 3.1.5 on 2021-02-03 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directmessages', '0003_auto_20210202_1737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='directmessage',
            options={'ordering': ['-sent'], 'verbose_name': 'DirectMessage', 'verbose_name_plural': 'DirectMessages'},
        ),
    ]
