# Generated by Django 4.0.8 on 2023-03-04 09:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0017_alter_hospital_service_hospital_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital_service',
            name='hospital_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
