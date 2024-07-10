from django import forms
from .models import UploadedFile, Material

class UploadFileForm(forms.ModelForm):
    file1 = forms.FileField(label='File Pertama')
    file2 = forms.FileField(label='File Kedua')

    class Meta:
        model = UploadedFile
        fields = ['file1', 'file2']

    def clean(self):
        cleaned_data = super().clean()
        file1 = cleaned_data.get('file1')
        file2 = cleaned_data.get('file2')

        if not file1:
            raise forms.ValidationError("File pertama tidak ditemukan.")
        if not file2:
            raise forms.ValidationError("File kedua tidak ditemukan.")

        if file1.name == file2.name:
            raise forms.ValidationError("Nama file pertama dan kedua tidak boleh sama.")

        if file1.size > 10 * 1024 * 1024 or file2.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Ukuran file terlalu besar. Maksimum 10 MB diizinkan.")

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'quantity']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
