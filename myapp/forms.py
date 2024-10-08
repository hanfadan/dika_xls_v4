from django import forms
from .models import UploadedFile, Material, CustomUser, MaterialRequest, UploadedMaterialRequestFile, ResultCompareData
from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(forms.Form):
    warehouse_data = forms.FileField(label='File Pertama')
    production_data = forms.FileField(label='File Kedua')

    def clean(self):
        cleaned_data = super().clean()
        file1 = cleaned_data.get('warehouse_data')
        file2 = cleaned_data.get('production_data')

        if not file1:
            raise forms.ValidationError("File pertama tidak ditemukan.")
        if not file2:
            raise forms.ValidationError("File kedua tidak ditemukan.")

        if file1.name == file2.name:
            raise forms.ValidationError("Nama file pertama dan kedua tidak boleh sama.")

        if file1.size > 10 * 1024 * 1024 or file2.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Ukuran file terlalu besar. Maksimum 10 MB diizinkan.")

class MaterialForm(forms.ModelForm):
    material_id = forms.CharField(label='Material ID', max_length=100, required=True)
    
    class Meta:
        model = Material
        fields = ['material_id', 'name', 'description', 'quantity']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

class MaterialRequestForm(forms.ModelForm):
    material_id = forms.CharField(max_length=100, label='Material ID', required=True)
    material_name = forms.CharField(max_length=100, label='Material Name')
    quantity = forms.IntegerField(label='Quantity')
    request_date = forms.DateField(label='Request Date', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = MaterialRequest
        fields = ['material_id', 'material_name', 'quantity', 'request_date']

class UploadMaterialRequestFileForm(forms.ModelForm):
    class Meta:
        model = UploadedMaterialRequestFile
        fields = ['file']

class ResultCompareDataForm(forms.ModelForm):
    class Meta:
        model = ResultCompareData
        fields = ['HU', 'Source_Handling_Unit']