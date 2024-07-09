from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='index'),  # Contoh pola URL untuk halaman beranda
    path('download/', views.download_comparison_excel, name='download_comparison_excel'),
    path('download/data', views.download_full_data, name='download_full_data'),
    path('materials/', views.material_list, name='material_list'),
    path('materials/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/new/', views.material_create, name='material_create'),
    path('materials/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('materials/<int:pk>/delete/', views.material_delete, name='material_delete'),
]
