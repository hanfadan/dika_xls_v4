from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='index'),  # Contoh pola URL untuk halaman beranda
    path('download/', views.download_comparison_excel, name='download_comparison_excel'),
    path('download/data', views.download_full_data, name='download_full_data'),

]
