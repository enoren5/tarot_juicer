from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_ui', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='An address or location text to display in the site footer. One entry is chosen at random per page load.')),
            ],
            options={
                'verbose_name': 'Footer Address',
                'verbose_name_plural': 'Footer Addresses',
            },
        ),
    ]
