# Generated by Django 3.1.5 on 2021-02-05 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Incedoinc', '0004_auto_20210205_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='feedback_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Incedoinc.feedback'),
        ),
    ]
