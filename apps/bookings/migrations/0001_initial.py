# Generated by Django 5.1.1 on 2024-10-23 15:34

import django.contrib.postgres.fields.ranges
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0006_rename_certifications_certification'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('num_hours', models.IntegerField(default=1)),
                ('subject', models.CharField(max_length=300)),
                ('user_needs', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('scheduled_for', models.DateTimeField()),
                ('time_range', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'paid')], default='pending', max_length=20)),
                ('is_done', models.BooleanField(default=False)),
                ('insightor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.insightor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
