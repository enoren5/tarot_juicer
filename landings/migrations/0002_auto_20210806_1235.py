# Generated by Django 3.2.4 on 2021-08-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutcontent',
            name='title',
            field=models.CharField(default='No title yet', max_length=256),
        ),
        migrations.AddField(
            model_name='essaylist',
            name='title',
            field=models.CharField(default='No title yet', max_length=256),
        ),
    ]
