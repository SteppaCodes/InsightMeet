# Generated by Django 5.1.1 on 2024-09-13 04:39

import django.db.models.deletion
import django_countries.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Insightor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('experience_years', models.IntegerField(default=0)),
                ('education', models.TextField(blank=True, null=True)),
                ('certifications', models.CharField(blank=True, max_length=255, null=True)),
                ('available', models.BooleanField(default=True)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('website_url', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('review', models.TextField()),
                ('insightor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.insightor')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
