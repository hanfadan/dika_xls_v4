import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import UploadFileForm
from django.http import HttpResponse
from .models import ResultCompareData
import numpy as np

import pandas as pd
import numpy as np

def compare_excel_files(file1_path, file2_path):
    try:
        # Membaca data dari file pertama
        df1 = pd.read_excel(file1_path, sheet_name='Recap', usecols=['HU', 'QTY'])
        
        # Membaca data dari file kedua
        df2 = pd.read_excel(file2_path, usecols=['Src Trgt Qty AUoM', 'Source Handling Unit'])
  
        # Mengubah DataFrame menjadi array untuk perbandingan
        arr_df1 = df1.astype(str).to_numpy()  # Mengonversi ke string
        arr_df2 = df2.astype(str).to_numpy()  # Mengonversi ke string
        
        # Membuat array untuk menyimpan hasil perbandingan
        comparison_result = []
        
        # Looping melalui setiap baris di arr_df1 untuk mencocokkan dengan arr_df2
        for row1 in arr_df1:
            hu1 = row1[0]  # HU dari arr_df1
            qty1 = row1[1] # QTY dari arr_df1
            
            # Jika HU dari df1 adalah 0, NaN, atau kosong, abaikan
            if hu1 in ['0', 'NaN', '']:
                continue
            
            # Mencari apakah HU dari arr_df1 ada di kolom "Source Handling Unit" di arr_df2
            matching_row_indices = np.where(arr_df2[:, 1] == hu1)[0]
            
            if len(matching_row_indices) == 0:
                # Jika tidak ditemukan HU yang cocok di df2
                comparison_result.append([hu1, qty1, '', '', 'Tidak ditemukan'])
            
            for index in matching_row_indices:
                source_handling_unit = arr_df2[index][1]  # Source Handling Unit dari arr_df2
                qty2 = arr_df2[index][0]  # Src Trgt Qty AUoM dari arr_df2
                
                # Membandingkan nilai QTY
                result = 'Cocok' if qty1 == qty2 else 'Tidak Cocok'
                
                # Menambahkan hasil perbandingan ke array comparison_result
                comparison_result.append([hu1, qty1, qty2, source_handling_unit, result])
        
        # Jika tidak ada data yang cocok ditemukan
        if len(comparison_result) == 0:
            comparison_result.append(['', '', '', '', 'Tidak ditemukan'])
        
        # Membuat DataFrame dari array comparison_result
        compared_data = pd.DataFrame(comparison_result, columns=['HU', 'QTY', 'Src_Trgt_Qty_AUoM', 'Source_Handling_Unit', 'Hasil_Perbandingan'])

        return compared_data
    except Exception as e:
        print("Error:", e)
        return pd.DataFrame(columns=['HU', 'QTY', 'Src_Trgt_Qty_AUoM', 'Source_Handling_Unit', 'Hasil_Perbandingan'])

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file1 = request.FILES['file1']
            uploaded_file2 = request.FILES['file2']
            
            # Menyimpan kedua file yang diunggah
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename1 = fs.save(uploaded_file1.name, uploaded_file1)
            filename2 = fs.save(uploaded_file2.name, uploaded_file2)

            # Melakukan perbandingan kedua file
            file1_path = fs.path(filename1)
            file2_path = fs.path(filename2)
            compared_data = compare_excel_files(file1_path, file2_path)
            
            # Menghapus kedua file yang diunggah dari sistem penyimpanan
            # fs.delete(filename1)
            # fs.delete(filename2)

            # Menyimpan data perbandingan ke database
            for index, row in compared_data.iterrows():
                result = ResultCompareData(
                    HU=row['HU'],
                    QTY=row['QTY'],
                    Src_Trgt_Qty_AUoM=row['Src_Trgt_Qty_AUoM'],
                    Source_Handling_Unit=row['Source_Handling_Unit'],
                    Hasil_Perbandingan=row['Hasil_Perbandingan']
                )
                result.save()

             # Simpan data perbandingan dalam sesi
            request.session['compared_data'] = compared_data.to_dict(orient='records')

            # Mengirimkan hasil perbandingan ke template
            return render(request, 'myapp/result.html', {'compared_data': compared_data})
    else:
        form = UploadFileForm()
    return render(request, 'myapp/upload.html', {'form': form})

def download_comparison_excel(request):
    # Dapatkan data perbandingan dari sesi
    compared_data = request.session.get('compared_data')

    # Buat DataFrame dari data perbandingan
    df = pd.DataFrame(compared_data)

    # Simpan DataFrame ke file Excel (XLSX)
    output_file = 'comparison_results.xlsx'
    df.to_excel(output_file, index=False)

    # Baca file Excel dan kirimkan sebagai respons HTTP
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response
    
def download_full_data(request):
    # Ambil semua data dari database
    all_data = ResultCompareData.objects.all()

    # Buat DataFrame dari data
    df = pd.DataFrame(list(all_data.values()))

    # Simpan DataFrame ke file Excel (XLSX)
    output_file = 'full_data_results.xlsx'
    df.to_excel(output_file, index=False)

    # Baca file Excel dan kirimkan sebagai respons HTTP
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response