from django.db import models
from django.contrib.auth.models import AbstractUser

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class ResultCompareData(models.Model):
    HU = models.CharField(max_length=100)
    QTY = models.CharField(max_length=100)
    Src_Trgt_Qty_AUoM = models.CharField(max_length=100)
    Source_Handling_Unit = models.CharField(max_length=100)
    Hasil_Perbandingan = models.CharField(max_length=100)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('supervisor', 'Supervisor'),
        ('production', 'Production Staff'),
        ('warehouse', 'Warehouse Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Tambahkan related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Tambahkan related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class MaterialRequest(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    request_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    file_url = models.CharField(max_length=255, blank=True, null=True)  # Add this line

    def __str__(self):
        return f"{self.material.name} requested by {self.requester.username}"
    
class UploadedMaterialRequestFile(models.Model):
    material_request = models.ForeignKey(MaterialRequest, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='material_request_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

