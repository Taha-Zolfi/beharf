# Generated by Django 4.1.5 on 2023-11-11 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_waiting_users_delete_calls'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCommunication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.JSONField(blank=True, null=True)),
                ('answer', models.JSONField(blank=True, null=True)),
                ('d', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]