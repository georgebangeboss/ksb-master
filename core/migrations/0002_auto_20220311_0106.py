# Generated by Django 3.2.12 on 2022-03-11 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyworksheet',
            name='work_sheet_images',
            field=models.FileField(blank=True, null=True, upload_to='work_sheet/'),
        ),
        migrations.CreateModel(
            name='FieldPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_image', models.FileField(blank=True, null=True, upload_to='field-photos/')),
                ('work_sheet_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='field_photos', to='core.dailyworksheet')),
            ],
        ),
    ]
