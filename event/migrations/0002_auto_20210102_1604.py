# Generated by Django 2.1 on 2021-01-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(max_length=4096),
        ),
    ]
