# Generated by Django 3.1.6 on 2021-03-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0035_auto_20210327_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rate',
            field=models.FloatField(null=True),
        ),
    ]
