import numpy as np
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, Http404
import os
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import LoginForm, UploadFileForm, MaterialForm, UserForm, MaterialRequestForm, UploadMaterialRequestFileForm
from .models import ResultCompareData, Material, MaterialRequest, CustomUser, Material
from .forms import ResultCompareDataForm
from django.core.paginator import Paginator

# Fungsi CRUD Material
@login_required
def material_list(request):
    comparison_data = ResultCompareData.objects.all()
    material_requests = MaterialRequest.objects.all()
    total_material_checked = comparison_data.count()
    material_request_sent = material_requests.count()

    context = {
        'comparison_data': comparison_data,
        'material_requests': material_requests,
        'total_material_checked': total_material_checked,
        'material_request_sent': material_request_sent,
    }

    return render(request, 'myapp/material_list.html', context)

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
    material = get_object_or_404(ResultCompareData, pk=pk)
    if request.method == 'POST':
        form = ResultCompareDataForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = ResultCompareDataForm(instance=material)
    return render(request, 'myapp/material_form.html', {'form': form})

@login_required
def material_delete(request, pk):
    material = get_object_or_404(ResultCompareData, pk=pk)
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
    total_material_checked = ResultCompareData.objects.count()
    material_request_sent = MaterialRequest.objects.count()
    return render(request, 'myapp/supervisor_dashboard.html', {
        'total_material_checked': total_material_checked,
        'material_request_sent': material_request_sent
    })

@login_required
def supervisor_view_users(request):
    users = User.objects.all()
    return render(request, 'myapp/supervisor_view_users.html', {'users': users})

@login_required
def supervisor_create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('view_division')
    else:
        form = UserForm()
    return render(request, 'myapp/supervisor_create_division.html', {'form': form})


@login_required
def supervisor_edit_user(request, username=None):
    user = None
    if username:
        user = get_object_or_404(CustomUser, username=username)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('view_division')
    else:
        form = UserForm(instance=user) if user else UserForm()

    return render(request, 'myapp/supervisor_edit_division.html', {'form': form, 'user': user})

@login_required
def supervisor_delete_user(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        if user_ids:
            CustomUser.objects.filter(id__in=user_ids).delete()
            return redirect('view_division')
    users = CustomUser.objects.all()
    return render(request, 'myapp/supervisor_delete_division.html', {'users': users})

@login_required
def production_dashboard(request):
    total_material_checked = ResultCompareData.objects.count()
    return render(request, 'myapp/production_dashboard.html', {'total_material_checked': total_material_checked})

@login_required
def warehouse_dashboard(request):
    total_material_request = MaterialRequest.objects.count()
    return render(request, 'myapp/warehouse_dashboard.html', {
        'total_material_request': total_material_request,
    })

@login_required
def warehouse_requested_material(request):
    materials = MaterialRequest.objects.select_related('material').all()
    return render(request, 'myapp/warehouse_requested_material.html', {'materials': materials})

@login_required
def warehouse_send_data(request, material_id=None):
    if material_id:
        material_request = get_object_or_404(MaterialRequest, pk=material_id)
    else:
        material_request = None

    if request.method == 'POST':
        form = UploadMaterialRequestFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            if material_request:
                uploaded_file.material_request = material_request
                uploaded_file.save()
                # Update the material request status and file_url
                material_request.status = 'done'
                material_request.file_url = uploaded_file.file.name  # Assuming the file field is 'file'
                material_request.save()

            return redirect('warehouse_requested_material')
    else:
        form = UploadMaterialRequestFileForm()

    return render(request, 'myapp/warehouse_send_data.html', {'form': form})

@login_required
def send_request(request):
    if request.method == 'POST':
        form = MaterialRequestForm(request.POST)
        if form.is_valid():
            material_id = form.cleaned_data['material_id']  # Ensure material_id is captured
            material_name = form.cleaned_data['material_name']
            quantity = form.cleaned_data['quantity']
            request_date = form.cleaned_data['request_date']

            # Check if the material already exists, if not create it
            material, created = Material.objects.get_or_create(
                material_id=material_id,  # Use material_id for lookup
                defaults={'name': material_name, 'description': 'Default description', 'quantity': quantity}
            )

            material_request = MaterialRequest(
                material=material,
                quantity=quantity,
                requester=request.user,
                request_date=request_date,
                status='pending',
            )
            material_request.save()
            return redirect('view_history')
    else:
        form = MaterialRequestForm()
    return render(request, 'myapp/supervisor_request_material.html', {'form': form})

@login_required
def view_history(request):
    material_requests = MaterialRequest.objects.all()
    return render(request, 'myapp/supervisor_view_history.html', {'material_requests': material_requests})

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
    
def production_download_data_view(request):
    return render(request, 'myapp/production_download_data.html')

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

@login_required
def production_compare_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file1 = request.FILES['warehouse_data']
            uploaded_file2 = request.FILES['production_data']

            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename1 = fs.save(uploaded_file1.name, uploaded_file1)
            filename2 = fs.save(uploaded_file2.name, uploaded_file2)

            file1_path = fs.path(filename1)
            file2_path = fs.path(filename2)
            compared_data = compare_excel_files(file1_path, file2_path)

            request.session['compared_data'] = compared_data.to_dict(orient='records')

            return redirect('production_compare_data')
    else:
        form = UploadFileForm()

    compared_data = request.session.get('compared_data', [])
    search_query = request.GET.get('search', '')

    filtered_data = compared_data
    if search_query:
        filtered_data = [row for row in compared_data if search_query.lower() in row['HU'].lower()]

    paginator = Paginator(filtered_data, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/production_check_data.html', {
        'form': form,
        'page_obj': page_obj,
        'search_query': search_query,
        'has_results': bool(filtered_data),
        'compared_data': compared_data
    })

@login_required
def download_comparison_excel(request):
    compared_data = request.session.get('compared_data')
    df = pd.DataFrame(compared_data)
    output_file = 'comparison_results.xlsx'
    df.to_excel(output_file, index=False)
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response

@login_required    
def download_full_data(request):
    all_data = ResultCompareData.objects.all()
    df = pd.DataFrame(list(all_data.values()))
    output_file = 'full_data_results.xlsx'
    df.to_excel(output_file, index=False)
    with open(output_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response

@login_required
def download_file(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
            return response
    raise Http404
