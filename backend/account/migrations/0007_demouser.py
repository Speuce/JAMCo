# Generated by Django 4.1.5 on 2023-03-06 02:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_user_friends"),
    ]

    operations = [
        migrations.CreateModel(
            name="DemoUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("birthday", models.DateField(null=True, verbose_name="Date of Birth")),
            ],
        ),
    ]
