# Generated by Django 3.2.4 on 2021-10-14 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_authtoggle_timeout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoggle',
            name='timeout',
            field=models.IntegerField(default=1),
        ),
    ]
