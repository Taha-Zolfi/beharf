# Generated by Django 4.1.5 on 2023-11-22 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_usercommunication_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCommunication_text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.JSONField(blank=True, null=True)),
                ('answer', models.JSONField(blank=True, null=True)),
                ('d', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='waiting_users_text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100000)),
            ],
        ),
    ]