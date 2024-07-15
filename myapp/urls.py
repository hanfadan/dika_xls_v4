from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('upload/', views.production_compare_data, name='upload_file'),
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
    # path('supervisor/create_user/', views.supervisor_create_user, name='supervisor_create_user'),
    # path('supervisor/edit_user/<int:user_id>/', views.supervisor_edit_user, name='supervisor_edit_user'),
    path('supervisor/delete_user/', views.supervisor_delete_user, name='supervisor_delete_user'),
    path('supervisor/send_request/', views.send_request, name='send_request'),
    path('supervisor/view_history/', views.view_history, name='view_history'),
    path('supervisor/view_division/', views.view_division, name='view_division'),
    path('supervisor/create_division/', views.supervisor_create_user, name='create_division'),
    re_path(r'^supervisor/edit_division(?:/(?P<username>[\w-]+))?/$', views.supervisor_edit_user, name='edit_division'),
    path('supervisor/delete_division/', views.supervisor_delete_user, name='delete_division'),

    # Production Staff URLs
    path('production_dashboard/', views.production_dashboard, name='production_dashboard'),
    path('production_check_data/', views.production_check_data, name='production_check_data'),
    path('production_compare_data/', views.production_compare_data, name='production_compare_data'),
    path('production_download_data_view/', views.production_download_data_view, name='production_download_data_view'),
    path('download_full_data/', views.download_full_data, name='download_full_data'),

    # Warehouse Staff URLs
    path('warehouse_dashboard/', views.warehouse_dashboard, name='warehouse_dashboard'),
    path('warehouse_requested_material/', views.warehouse_requested_material, name='warehouse_requested_material'),
    re_path(r'^warehouse/send_data(?:/(?P<material_id>\d+))?/$', views.warehouse_send_data, name='warehouse_send_data'),
]
