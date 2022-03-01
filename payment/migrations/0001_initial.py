# Generated by Django 2.1.5 on 2019-01-13 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("branch", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("value", models.FloatField()),
                ("expiration_date", models.DateField()),
                ("date_payment", models.DateField(null=True)),
                ("is_paid", models.BooleanField(default=False)),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="branch.Branch"
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
                "db_table": "payment",
            },
        ),
    ]
