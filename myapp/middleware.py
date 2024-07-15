from django.shortcuts import redirect
from django.urls import reverse

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_role = request.user.role
            path = request.path

            # Define role-based access here
            role_paths = {
                'supervisor': [
                    reverse('supervisor_dashboard'),
                    reverse('supervisor_view_users'),
                    reverse('supervisor_create_user'),
                    # Add other supervisor paths here
                ],
                'production': [
                    reverse('production_dashboard'),
                    reverse('production_check_data'),
                    reverse('production_download_data_view'),
                    # Add other production paths here
                ],
                'warehouse': [
                    reverse('warehouse_dashboard'),
                    reverse('warehouse_requested_material'),
                    reverse('warehouse_send_data'),
                    # Add other warehouse paths here
                ],
            }

            allowed_paths = role_paths.get(user_role, [])

            if path not in allowed_paths and not path.startswith(reverse('admin:index')):
                # Redirect to a 403 Forbidden page or some other page
                return redirect('forbidden_page')

        response = self.get_response(request)
        return response
