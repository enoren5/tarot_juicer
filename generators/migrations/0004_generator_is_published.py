# Generated by Django 3.2.12 on 2022-11-07 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generators', '0003_auto_20210423_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='generator',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
