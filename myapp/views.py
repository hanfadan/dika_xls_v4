import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import UploadFileForm, MaterialForm
from django.http import HttpResponse
from .models import ResultCompareData, Material
import numpy as np

def compare_excel_files(file1_path, file2_path):
    try:
        df1 = pd.read_excel(file1_path, sheet_name='Recap', usecols=['HU', 'QTY'])
        df2 = pd.read_excel(file2_path, usecols=['Src Trgt Qty AUoM', 'Source Handling Unit'])
        arr_df1 = df1.astype(str).to_numpy()
        arr_df2 = df2.astype(str).to_numpy()
        comparison_result = []

        for row1 in arr_df1:
            hu1 = row1[0]
            qty1 = row1[1]
            if hu1 in ['0', 'NaN', '']:
                continue
            matching_row_indices = np.where(arr_df2[:, 1] == hu1)[0]
            if len(matching_row_indices) == 0:
                comparison_result.append([hu1, qty1, '', '', 'Tidak ditemukan'])
            for index in matching_row_indices:
                source_handling_unit = arr_df2[index][1]
                qty2 = arr_df2[index][0]
                result = 'Cocok' if qty1 == qty2 else 'Tidak Cocok'
                comparison_result.append([hu1, qty1, qty2, source_handling_unit, result])

        if len(comparison_result) == 0:
            comparison_result.append(['', '', '', '', 'Tidak ditemukan'])

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
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename1 = fs.save(uploaded_file1.name, uploaded_file1)
            filename2 = fs.save(uploaded_file2.name, uploaded_file2)
            file1_path = fs.path(filename1)
            file2_path = fs.path(filename2)
            compared_data = compare_excel_files(file1_path, file2_path)

            for index, row in compared_data.iterrows():
                result = ResultCompareData(
                    HU=row['HU'],
                    QTY=row['QTY'],
                    Src_Trgt_Qty_AUoM=row['Src_Trgt_Qty_AUoM'],
                    Source_Handling_Unit=row['Source_Handling_Unit'],
                    Hasil_Perbandingan=row['Hasil_Perbandingan']
                )
                result.save()

            request.session['compared_data'] = compared_data.to_dict(orient='records')
            return render(request, 'myapp/result.html', {'compared_data': compared_data})
    else:
        form = UploadFileForm()
    return render(request, 'myapp/upload.html', {'form': form})

def download_comparison_excel(request):
    compared_data = request.session.get('compared_data')
    df = pd.DataFrame(compared_data)
    output_file = 'comparison_results.xlsx'
    df.to_excel(output_file, index=False)
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response

def download_full_data(request):
    all_data = ResultCompareData.objects.all()
    df = pd.DataFrame(list(all_data.values()))
    output_file = 'full_data_results.xlsx'
    df.to_excel(output_file, index=False)
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response

# Fungsi CRUD Material
def material_list(request):
    materials = Material.objects.all()
    return render(request, 'myapp/material_list.html', {'materials': materials})

def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'myapp/material_detail.html', {'material': material})

def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'myapp/material_form.html', {'form': form})

def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'myapp/material_form.html', {'form': form})

def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('material_list')
    return render(request, 'myapp/material_confirm_delete.html', {'material': material})
