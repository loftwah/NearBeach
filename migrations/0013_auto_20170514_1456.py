# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-14 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('NearBeach', '0012_documents_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='document_location',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='image',
        ),
        migrations.AddField(
            model_name='documents',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.AddField(
            model_name='documents',
            name='document_uploaded_audit',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documents',
            name='document_url_location',
            field=models.TextField(blank=True, null=True),
        ),
    ]