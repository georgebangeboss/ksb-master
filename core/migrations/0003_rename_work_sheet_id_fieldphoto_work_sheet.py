# Generated by Django 3.2.12 on 2022-03-11 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220311_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldphoto',
            old_name='work_sheet_id',
            new_name='work_sheet',
        ),
    ]
