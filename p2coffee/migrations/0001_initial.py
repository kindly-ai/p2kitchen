# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 20:45
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SensorEvent",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=254)),
                ("value", models.CharField(max_length=254)),
                ("id", models.CharField(max_length=254)),
            ],
            options={
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "abstract": False,
            },
        ),
    ]
