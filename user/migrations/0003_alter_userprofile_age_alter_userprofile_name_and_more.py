# Generated by Django 4.2.4 on 2023-08-28 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_basicauthentication_userprofile_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='BasicAuthentication',
        ),
    ]
