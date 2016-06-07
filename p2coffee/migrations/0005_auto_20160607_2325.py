# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2coffee', '0004_auto_20160524_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coffeepotevent',
            options={'ordering': ['created'], 'verbose_name': 'Coffee pot event', 'verbose_name_plural': 'Coffee pot events'},
        ),
        migrations.AlterModelOptions(
            name='sensorevent',
            options={'ordering': ['created'], 'verbose_name': 'Sensor event', 'verbose_name_plural': 'Sensor events'},
        ),
        migrations.AddField(
            model_name='coffeepotevent',
            name='slack_channel',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='coffeepotevent',
            name='slack_ts',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='coffeepotevent',
            name='type',
            field=models.CharField(choices=[('brew_started', 'I started brewing'), ('brew_finished', "I'm done brewing")], max_length=254),
        ),
    ]
