# Generated by Django 5.1.1 on 2024-09-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insightor',
            name='hourly_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
