# Generated by Django 3.1.5 on 2021-02-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Incedoinc', '0003_auto_20210206_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='field_name',
            field=models.CharField(max_length=20),
        ),
    ]