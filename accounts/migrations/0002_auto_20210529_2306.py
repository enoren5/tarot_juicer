# Generated by Django 3.1.6 on 2021-05-29 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtoggle',
            name='nuclear',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='authtoggle',
            name='swap_html',
            field=models.BooleanField(default=False),
        ),
    ]