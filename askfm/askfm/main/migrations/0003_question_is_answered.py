# Generated by Django 3.0.6 on 2020-05-09 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200509_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_answered',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
