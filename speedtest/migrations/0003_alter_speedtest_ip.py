# Generated by Django 4.2.4 on 2023-08-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speedtest', '0002_alter_speedtest_ip_alter_speedtest_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speedtest',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1', null=True),
        ),
    ]
