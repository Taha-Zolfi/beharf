# Generated by Django 4.1.5 on 2023-11-11 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_usercommunication'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercommunication',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]