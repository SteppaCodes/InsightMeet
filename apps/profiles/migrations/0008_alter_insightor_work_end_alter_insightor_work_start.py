# Generated by Django 5.1.1 on 2024-10-25 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_insightor_available_days_insightor_work_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insightor',
            name='work_end',
            field=models.TimeField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='insightor',
            name='work_start',
            field=models.TimeField(blank=True, max_length=15, null=True),
        ),
    ]
