# Generated by Django 3.2.14 on 2022-11-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landings', '0005_auto_20221107_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutcontent',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='essaylist',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='howto',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
