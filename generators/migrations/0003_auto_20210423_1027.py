# Generated by Django 3.1.6 on 2021-04-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generators', '0002_auto_20210402_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generator',
            name='description_bullets',
            field=models.TextField(blank=True, help_text='Please use line space for bullet points', null=True),
        ),
    ]
