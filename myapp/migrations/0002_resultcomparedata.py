# Generated by Django 5.0.4 on 2024-05-01 16:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResultCompareData",
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
                ("HU", models.CharField(max_length=100)),
                ("QTY", models.IntegerField()),
                ("Src_Trgt_Qty_AUoM", models.IntegerField()),
                ("Source_Handling_Unit", models.CharField(max_length=100)),
                ("Hasil_Perbandingan", models.CharField(max_length=100)),
            ],
        ),
    ]
