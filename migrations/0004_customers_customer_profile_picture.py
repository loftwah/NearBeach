# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-26 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0003_contact_history_contact_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='customer_profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
