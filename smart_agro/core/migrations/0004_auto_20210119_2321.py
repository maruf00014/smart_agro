# Generated by Django 3.1.5 on 2021-01-19 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_soildata_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soildata',
            old_name='n_time',
            new_name='time',
        ),
    ]
