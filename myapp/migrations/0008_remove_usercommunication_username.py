# Generated by Django 4.1.5 on 2023-11-17 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_usercommunication_remove_waiting_users_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercommunication',
            name='username',
        ),
    ]
