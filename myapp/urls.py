from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/', views.download_comparison_excel, name='download_comparison_excel'),
    path('download/data', views.download_full_data, name='download_full_data'),
    
    # Materials CRUD URLs
    path('materials/', views.material_list, name='material_list'),
    path('materials/new/', views.material_create, name='material_create'),
    path('materials/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('materials/<int:pk>/delete/', views.material_delete, name='material_delete'),

    # Supervisor URLs
    path('supervisor_dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('supervisor/view_users/', views.supervisor_view_users, name='supervisor_view_users'),
    path('supervisor/create_user/', views.supervisor_create_user, name='supervisor_create_user'),
    path('supervisor/edit_user/<int:user_id>/', views.supervisor_edit_user, name='supervisor_edit_user'),
    path('supervisor/delete_user/', views.supervisor_delete_user, name='supervisor_delete_user'),
    path('supervisor/send_request/', views.send_request, name='send_request'),
    path('supervisor/view_history/', views.view_history, name='view_history'),
    path('supervisor/view_division/', views.view_division, name='view_division'),
    path('supervisor/create_division/', views.create_division, name='create_division'),
    path('supervisor/edit_division/', views.edit_division, name='edit_division'),
    path('supervisor/delete_division/', views.delete_division, name='delete_division'),

    # Production Staff URLs
    path('production_dashboard/', views.production_dashboard, name='production_dashboard'),

    # Warehouse Staff URLs
    path('warehouse_dashboard/', views.warehouse_dashboard, name='warehouse_dashboard'),
]
