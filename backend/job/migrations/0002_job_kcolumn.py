# Generated by Django 4.1.5 on 2023-02-17 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_user_region"),
        ("job", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="kcolumn",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.kanbancolumn",
            ),
            preserve_default=False,
        ),
    ]
