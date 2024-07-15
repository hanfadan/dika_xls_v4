import numpy as np
import pandas as pd
import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import LoginForm, UploadFileForm, MaterialForm, UserForm
from .models import ResultCompareData, Material, MaterialRequest, CustomUser

# Fungsi CRUD Material
@login_required
def material_list(request):
    materials = Material.objects.all()
    total_material_checked = materials.count()
    material_request_sent = MaterialRequest.objects.filter(requester=request.user).count()

    return render(request, 'myapp/material_list.html', {
        'materials': materials,
        'total_material_checked': total_material_checked,
        'material_request_sent': material_request_sent,
    })

@login_required
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'myapp/material_detail.html', {'material': material})

@login_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'myapp/material_form.html', {'form': form})

@login_required
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

@login_required
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        return redirect('material_list')
    return render(request, 'myapp/material_confirm_delete.html', {'material': material})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'supervisor':
                    return redirect('supervisor_dashboard')
                elif user.role == 'production':
                    return redirect('production_dashboard')
                elif user.role == 'warehouse':
                    return redirect('warehouse_dashboard')
                else:
                    form.add_error(None, 'User role is not defined')
            else:
                form.add_error(None, 'Username or password is incorrect')
    return render(request, 'myapp/login.html', {'form': form})

User = get_user_model()

@login_required
def supervisor_dashboard(request):
    return render(request, 'myapp/supervisor_dashboard.html')

@login_required
def supervisor_view_users(request):
    users = User.objects.all()
    return render(request, 'myapp/supervisor_view_users.html', {'users': users})

@login_required
def supervisor_create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('supervisor_view_users')
    else:
        form = UserForm()
    return render(request, 'myapp/supervisor_create_user.html', {'form': form})

@login_required
def supervisor_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('supervisor_view_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'myapp/supervisor_edit_user.html', {'form': form})

@login_required
def supervisor_delete_user(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        User.objects.filter(id__in=user_ids).delete()
        messages.success(request, 'Users deleted successfully')
        return redirect('supervisor_view_users')
    users = User.objects.all()
    return render(request, 'myapp/supervisor_delete_user.html', {'users': users})

@login_required
def production_dashboard(request):
    total_material_checked = Material.objects.count()
    return render(request, 'myapp/production_dashboard.html', {'total_material_checked': total_material_checked})

@login_required
def warehouse_dashboard(request):
    total_material_request = MaterialRequest.objects.count()
    return render(request, 'myapp/warehouse_dashboard.html', {'total_material_request': total_material_request})

@login_required
def warehouse_requested_material(request):
    materials = MaterialRequest.objects.all()  # Adjust the query as needed
    return render(request, 'myapp/warehouse_requested_material.html', {'materials': materials})

@login_required
def warehouse_send_data(request):
    if request.method == 'POST':
        material_data = request.FILES['material_data']
        # Process the uploaded file as needed
        # Save the data to the database or perform any other necessary actions
        messages.success(request, 'Data material sent successfully.')
        return redirect('warehouse_requested_material')
    return render(request, 'myapp/warehouse_send_data.html')


@login_required
def send_request(request):
    if request.method == 'POST':
        material_name = request.POST.get('material_name')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')
        
        # Simpan permintaan material ke database
        MaterialRequest.objects.create(
            requester=request.user,
            material_name=material_name,
            quantity=quantity,
            date=date
        )
        
        messages.success(request, 'Request sent successfully')
        return redirect('view_history')
    return render(request, 'myapp/supervisor_request_material.html')

@login_required
def view_history(request):
    materials = MaterialRequest.objects.all()
    return render(request, 'myapp/supervisor_view_history.html', {'materials': materials})

@login_required
def view_division(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
        'total_divisions': users.count(),
        'active_divisions': users.filter(is_active=True).count()
    }
    return render(request, 'myapp/supervisor_view_division.html', context)


@login_required
def create_division(request):
    if request.method == 'POST':
        return redirect('view_division')
    return render(request, 'myapp/supervisor_create_division.html')

@login_required
def edit_division(request):
    if request.method == 'POST':
        return redirect('view_division')
    return render(request, 'myapp/supervisor_edit_division.html')

@login_required
def delete_division(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        User.objects.filter(id__in=user_ids).delete()
        messages.success(request, 'Users deleted successfully')
        return redirect('supervisor_view_users')
    
    users = CustomUser.objects.all()
    return render(request, 'myapp/supervisor_delete_division.html', {'users': users})

@login_required
def production_check_data(request):
    materials = Material.objects.all()
    return render(request, 'myapp/production_check_data.html', {'materials': materials})

@login_required
def production_download_data(request):
    materials = Material.objects.all()
    df = pd.DataFrame(list(materials.values()))
    output_file = 'material_data.xlsx'
    df.to_excel(output_file, index=False)
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response

@login_required
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

@login_required
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

@login_required
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

def production_download_data_view(request):
    return render(request, 'myapp/production_download_data.html')

@login_required    
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
