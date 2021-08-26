# Generated by Django 3.2.6 on 2021-08-26 11:30

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("p2coffee", "0005_auto_20160607_2325"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brew",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "brewer_slack_username",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "finished_event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brews_finished",
                        to="p2coffee.coffeepotevent",
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Machine",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("device_name", models.CharField(max_length=255)),
                (
                    "volume",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=1.25, max_digits=4
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("brewing", "Brewing"), ("idle", "Idle")],
                        default="idle",
                        max_length=7,
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="sensorevent",
            name="name",
            field=models.CharField(
                choices=[
                    ("power-switch", "Power switched"),
                    ("power-meter-has-changed", "Power meter changed"),
                    ("power-meter", "Power metered"),
                ],
                max_length=254,
            ),
        ),
        migrations.CreateModel(
            name="BrewReaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("reaction", models.CharField(max_length=255)),
                ("is_custom_reaction", models.BooleanField(blank=True, default=False)),
                ("slack_username", models.CharField(max_length=255)),
                (
                    "brew",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="p2coffee.brew"
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="brew",
            name="machine",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="p2coffee.machine"
            ),
        ),
        migrations.AddField(
            model_name="brew",
            name="started_event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="brews_started",
                to="p2coffee.coffeepotevent",
            ),
        ),
        migrations.AddField(
            model_name="coffeepotevent",
            name="machine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="p2coffee.machine",
            ),
        ),
        migrations.AddField(
            model_name="sensorevent",
            name="machine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="p2coffee.machine",
            ),
        ),
    ]
