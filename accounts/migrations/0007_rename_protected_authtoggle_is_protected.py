# Generated by Django 3.2.4 on 2021-11-02 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_on_authtoggle_protected'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authtoggle',
            old_name='protected',
            new_name='is_protected',
        ),
    ]
