from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.login_view, name='login'),  # Mengatur login sebagai halaman utama
    path('upload/', views.upload_file, name='upload_file'),
    path('download/', views.download_comparison_excel, name='download_comparison_excel'),
    path('download/data', views.download_full_data, name='download_full_data'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/new/', views.material_create, name='material_create'),
    path('materials/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('materials/<int:pk>/delete/', views.material_delete, name='material_delete'),
    path('supervisor_dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('send_request/', views.send_request, name='send_request'),
    path('view_history/', views.view_history, name='view_history'),
    path('view_division/', views.view_division, name='view_division'),
    path('create_division/', views.create_division, name='create_division'),
    path('edit_division/', views.edit_division, name='edit_division'),
    path('delete_division/', views.delete_division, name='delete_division'),
]
