# Generated by Django 4.0.3 on 2022-06-22 09:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_disease_alter_appointment_date_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Disease',
        ),
        migrations.AddField(
            model_name='specialty',
            name='desc',
            field=models.TextField(default='demo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 24, 9, 14, 57, 202762, tzinfo=utc), null=True),
        ),
    ]
