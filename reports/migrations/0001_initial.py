# Generated by Django 3.0.4 on 2020-04-13 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('amount', models.FloatField(max_length=255)),
                ('client', models.CharField(max_length=255)),
                ('purpose', models.CharField(choices=[('MORTGAGE', 'MORTGAGE'), (
                    'EXPROPRIATION', 'EXPROPRIATION'), ('EVALUATION', 'EVALUATION')], max_length=100)),
                ('inspection_date', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('plot_no', models.CharField(max_length=255, unique=True)),
                ('report_payed_for', models.BooleanField(default=False)),
                ('reason_for_not_paying', models.TextField()),
                ('delivery_date', models.CharField(max_length=255)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('report_file', models.FileField(upload_to='documents')),
                ('paid', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(max_length=255,
                                                 on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(max_length=255,
                                                 on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='comments', to='reports.Report')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
