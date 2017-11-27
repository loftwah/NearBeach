# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 07:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NearBeach', '0020_auto_20171127_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='list_of_quote_approval_status',
            fields=[
                ('quote_approval_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('quote_approval_status', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=5)),
                ('change_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_of_quote_approval_status_change_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'list_of_quote_approval_status',
            },
        ),
        migrations.CreateModel(
            name='list_of_quote_stages',
            fields=[
                ('quote_stages_id', models.AutoField(primary_key=True, serialize=False)),
                ('quote_stage', models.CharField(max_length=50)),
                ('is_invoice', models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=5)),
                ('change_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_of_quote_stages_change_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'list_of_quote_stages',
            },
        ),
        migrations.RemoveField(
            model_name='quote_approval_status',
            name='change_user',
        ),
        migrations.RemoveField(
            model_name='quote_stages',
            name='change_user',
        ),
        migrations.AlterField(
            model_name='quotes',
            name='quote_approval_status_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NearBeach.list_of_quote_approval_status'),
        ),
        migrations.AlterField(
            model_name='quotes',
            name='quote_stage_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NearBeach.list_of_quote_stages'),
        ),
        migrations.DeleteModel(
            name='quote_approval_status',
        ),
        migrations.DeleteModel(
            name='quote_stages',
        ),
    ]
