# Generated by Django 5.0.4 on 2024-07-15 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_materialrequest_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedMaterialRequestFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='material_request_files/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('material_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_files', to='myapp.materialrequest')),
            ],
        ),
    ]
