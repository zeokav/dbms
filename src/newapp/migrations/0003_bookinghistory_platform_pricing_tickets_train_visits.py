# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0002_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingHistory',
            fields=[
                ('pnr', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'booking_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('platform_id', models.IntegerField(primary_key=True, serialize=False)),
                ('platform_name', models.CharField(max_length=50)),
                ('xcoord', models.IntegerField()),
                ('ycoord', models.IntegerField()),
            ],
            options={
                'db_table': 'platform',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_fare', models.FloatField(blank=True, null=True)),
                ('cost_per_km', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'pricing',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('pnr', models.IntegerField(primary_key=True, serialize=False)),
                ('no_of_platforms', models.IntegerField(blank=True, null=True)),
                ('journey_distance', models.FloatField(blank=True, null=True)),
                ('date_of_journey', models.DateField(blank=True, null=True)),
                ('startplatform_id', models.IntegerField(blank=True, null=True)),
                ('endplatform_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tickets',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('train_name', models.CharField(max_length=30)),
                ('train_id', models.IntegerField(primary_key=True, serialize=False)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('startp_id', models.IntegerField(blank=True, null=True)),
                ('endp_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'train',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.CharField(max_length=8)),
                ('arrival_time', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'visits',
                'managed': False,
            },
        ),
    ]