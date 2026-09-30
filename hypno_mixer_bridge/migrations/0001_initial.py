from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preamble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('author', models.CharField(blank=True, max_length=30)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Preambles (hypno_mixer)',
                'db_table': 'contents_preamble',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Induction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=30)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Inductions (hypno_mixer)',
                'db_table': 'contents_induction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ScriptSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Scripting - Custom (hypno_mixer)',
                'db_table': 'contents_scriptsuggestion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Research (hypno_mixer)',
                'db_table': 'contents_research',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StockScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Scripting - Stock (hypno_mixer)',
                'db_table': 'contents_stockscript',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NYTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
            ],
            options={
                'verbose_name_plural': 'NY Times (hypno_mixer)',
                'db_table': 'contents_nytimes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TorStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
            ],
            options={
                'verbose_name_plural': 'Toronto Star (hypno_mixer)',
                'db_table': 'contents_torstar',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WSJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('essential', models.BooleanField(blank=True, default=False)),
                ('author', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True)),
                ('body', models.TextField(blank=True, max_length=300000)),
            ],
            options={
                'verbose_name_plural': 'WSJ (hypno_mixer)',
                'db_table': 'contents_wsjournal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssortedPeriodicals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(blank=True, max_length=300)),
                ('author_last_name', models.CharField(blank=True, max_length=300)),
                ('publication_year', models.CharField(blank=True, max_length=300)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('title', models.CharField(blank=True, max_length=300)),
            ],
            options={
                'verbose_name_plural': 'Assorted Periodicals (hypno_mixer)',
                'db_table': 'contents_assortedperiodicals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssortedLiterature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(blank=True, max_length=300)),
                ('author_last_name', models.CharField(blank=True, max_length=300)),
                ('publication_year', models.CharField(blank=True, max_length=300)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('title', models.CharField(blank=True, max_length=300)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Assorted Literature (hypno_mixer)',
                'db_table': 'contents_assortedliterature',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Binaurals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_last_name', models.CharField(blank=True, max_length=300)),
                ('publication_year', models.CharField(blank=True, max_length=300)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('title', models.CharField(blank=True, max_length=300)),
                ('publication_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Binaurals (hypno_mixer)',
                'db_table': 'contents_binaurals',
                'managed': False,
            },
        ),
    ]
