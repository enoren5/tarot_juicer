# Generated by Django 5.1.7 on 2025-07-20 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generators', '0017_alter_generator_tarot_card_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generator',
            name='tarot_card_non_imgur_image',
            field=models.ImageField(blank=True, upload_to='banned_from_imgur/'),
        ),
    ]
