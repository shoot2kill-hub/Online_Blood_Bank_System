# Generated by Django 4.0.8 on 2023-02-28 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0008_remove_blooddonate_bloodpressure'),
    ]

    operations = [
        migrations.AddField(
            model_name='blooddonate',
            name='gender',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
