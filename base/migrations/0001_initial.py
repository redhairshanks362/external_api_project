# Generated by Django 4.2.4 on 2023-08-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NASAApod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('explanation', models.TextField(null=True)),
                ('hdurl', models.URLField()),
                ('media_type', models.CharField(max_length=200)),
                ('service_version', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('url', models.URLField(null=True)),
            ],
        ),
    ]
