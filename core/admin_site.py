from django.contrib.admin import AdminSite
from users.admin import *
from users.models import OtpCode


class CustomAdminSite(AdminSite):
    site_header = 'Admin'
    site_title = 'Admin'

    def __init__(self, name='admin'):
        super().__init__(name)

    def has_permission(self, request):
        return request.user.is_superuser


admin_site = CustomAdminSite()

admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(OtpCode)
