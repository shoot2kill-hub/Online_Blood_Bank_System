# Generated by Django 4.0.8 on 2023-02-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0003_rename_email_donor_bloodgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='bloodgroup',
        ),
        migrations.AddField(
            model_name='donor',
            name='email',
            field=models.CharField(default=25, max_length=25),
            preserve_default=False,
        ),
    ]
