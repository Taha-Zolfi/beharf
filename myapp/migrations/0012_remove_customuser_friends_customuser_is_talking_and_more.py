# Generated by Django 4.1.5 on 2023-12-02 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_remove_friendrequest_accepted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='friends',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_talking',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='FriendRequest',
        ),
    ]
