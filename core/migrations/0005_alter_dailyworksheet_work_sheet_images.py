# Generated by Django 3.2.12 on 2022-03-11 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_dailyworksheet_work_sheet_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworksheet',
            name='work_sheet_images',
            field=models.FileField(blank=True, null=True, upload_to='worksheets/'),
        ),
    ]
