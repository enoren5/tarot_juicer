# Generated by Django 3.2.4 on 2021-10-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landings', '0003_auto_20210806_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='HowTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='How to use this website', max_length=256)),
                ('text_content', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='essaylist',
            name='title',
            field=models.CharField(default='Essay list', max_length=256),
        ),
    ]
