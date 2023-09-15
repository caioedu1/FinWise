# Generated by Django 4.2.5 on 2023-09-14 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_user_password1_user_password2_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cash',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
