# Generated by Django 4.0.8 on 2023-02-27 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donor',
            old_name='bloodgroup',
            new_name='email',
        ),
    ]
