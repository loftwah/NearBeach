# Generated by Django 2.1 on 2018-10-15 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0009_auto_20181015_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_campus',
            name='customer_fax',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer_campus',
            name='customer_phone',
            field=models.CharField(max_length=20),
        ),
    ]
