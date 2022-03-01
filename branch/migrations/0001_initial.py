# Generated by Django 2.1.5 on 2019-01-13 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Branch",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("current_balance", models.FloatField()),
                ("previous_balance", models.FloatField(null=True)),
            ],
            options={
                "verbose_name": "Branch",
                "verbose_name_plural": "Branches",
                "db_table": "branch",
            },
        ),
    ]
