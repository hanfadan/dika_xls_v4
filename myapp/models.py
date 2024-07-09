from django.db import models

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