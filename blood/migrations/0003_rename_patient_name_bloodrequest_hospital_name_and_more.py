# Generated by Django 4.0.8 on 2023-03-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0002_bloodrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='patient_name',
            new_name='hospital_name',
        ),
        migrations.RemoveField(
            model_name='bloodrequest',
            name='patient_age',
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='address',
            field=models.CharField(default=30, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='mobile',
            field=models.CharField(default=20, max_length=20),
            preserve_default=False,
        ),
    ]
