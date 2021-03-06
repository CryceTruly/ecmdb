# Generated by Django 3.0.4 on 2020-04-13 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone_number', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'About Company',
            },
        ),
    ]
