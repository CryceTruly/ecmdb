# Generated by Django 3.0.3 on 2020-03-09 17:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_report_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='delivery_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
