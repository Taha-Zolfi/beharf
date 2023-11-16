# Generated by Django 4.1.5 on 2023-10-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='calls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=100000)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_talking',
            field=models.BooleanField(default=False),
        ),
    ]
