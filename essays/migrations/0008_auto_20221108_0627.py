# Generated by Django 3.2.14 on 2022-11-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essays', '0007_auto_20221107_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliographyarticle',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contentchanges',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='curatedslashdot',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='curatedwatchtower',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]