# Generated by Django 5.1.1 on 2024-10-24 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
        ('profiles', '0006_rename_certifications_certification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='insightor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='profiles.insightor'),
        ),
    ]