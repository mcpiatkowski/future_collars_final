# Generated by Django 3.1.6 on 2021-04-01 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0041_auto_20210330_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='month',
            field=models.DateField(),
        ),
    ]