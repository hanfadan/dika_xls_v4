# Generated by Django 5.0.4 on 2024-05-01 16:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_resultcomparedata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resultcomparedata",
            name="QTY",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="resultcomparedata",
            name="Src_Trgt_Qty_AUoM",
            field=models.CharField(max_length=100),
        ),
    ]
