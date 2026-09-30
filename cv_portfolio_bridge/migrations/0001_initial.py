from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('tagline', models.CharField(blank=True, max_length=200)),
                ('preamble_heading', models.CharField(blank=True, max_length=100)),
                ('preamble_text', models.TextField(blank=True)),
                ('time_logger_heading', models.CharField(blank=True, max_length=100)),
                ('time_logger_text', models.TextField(blank=True)),
                ('core_research_heading', models.CharField(blank=True, max_length=100)),
                ('core_research_text', models.TextField(blank=True)),
                ('certifications_heading', models.CharField(blank=True, max_length=100)),
                ('certifications_text', models.TextField(blank=True)),
                ('about_heading', models.CharField(blank=True, max_length=100)),
                ('about_text', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Profile (CV_Portfolio)',
                'db_table': 'portfolio_profile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(blank=True, max_length=150)),
                ('quote', models.TextField()),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Testimonials (CV_Portfolio)',
                'db_table': 'portfolio_testimonial',
                'ordering': ['order'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=220)),
                ('author', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('excerpt', models.TextField()),
                ('body', models.TextField()),
                ('published_at', models.DateField()),
                ('is_published', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Showcase Samples (CV_Portfolio)',
                'db_table': 'portfolio_sample',
                'ordering': ['order'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FurtherResearchSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=220)),
                ('author', models.CharField(max_length=100)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('excerpt', models.TextField()),
                ('body', models.TextField()),
                ('published_at', models.DateField()),
                ('is_published', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Further Research Samples (CV_Portfolio)',
                'db_table': 'portfolio_furtherresearchsample',
                'ordering': ['order'],
                'managed': False,
            },
        ),
    ]
