# Generated by Django 3.2.7 on 2021-09-08 19:29

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("p2coffee", "0006_auto_20210826_1330"),
    ]

    operations = [
        migrations.CreateModel(
            name="SlackProfile",
            fields=[
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name="modified"),
                ),
                ("user_id", models.CharField(max_length=255, primary_key=True, serialize=False)),
                ("display_name", models.CharField(blank=True, default="", max_length=255)),
                ("real_name", models.CharField(blank=True, default="", max_length=255)),
                ("image_original", models.CharField(blank=True, default="", max_length=255)),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="brew",
            name="brewer_slack_username",
        ),
        migrations.RemoveField(
            model_name="brewreaction",
            name="slack_username",
        ),
        migrations.AddField(
            model_name="brew",
            name="slack_channel",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="brew",
            name="slack_ts",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="brew",
            name="status",
            field=models.CharField(
                choices=[("brewing", "Brewing"), ("finished", "Finished")], default="brewing", max_length=8
            ),
        ),
        migrations.AddField(
            model_name="machine",
            name="avatar_path",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AlterField(
            model_name="brew",
            name="finished_event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="brews_finished",
                to="p2coffee.sensorevent",
            ),
        ),
        migrations.AlterField(
            model_name="brew",
            name="machine",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="brews", to="p2coffee.machine"
            ),
        ),
        migrations.AlterField(
            model_name="brew",
            name="started_event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="brews_started", to="p2coffee.sensorevent"
            ),
        ),
        migrations.AlterField(
            model_name="brewreaction",
            name="brew",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to="p2coffee.brew"
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="device_name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="sensorevent",
            name="id",
            field=models.CharField(help_text="Device ID", max_length=254),
        ),
        migrations.AddField(
            model_name="brew",
            name="brewer",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="p2coffee.slackprofile"
            ),
        ),
        migrations.AddField(
            model_name="brewreaction",
            name="user",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="p2coffee.slackprofile"
            ),
        ),
    ]
