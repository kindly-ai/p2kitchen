# Generated by Django 3.2.7 on 2021-09-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("p2coffee", "0008_sensorevent_device_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brew",
            name="status",
            field=models.CharField(
                choices=[("brewing", "Brewing"), ("finished", "Finished"), ("invalid", "Invalid")],
                default="brewing",
                max_length=8,
            ),
        ),
    ]