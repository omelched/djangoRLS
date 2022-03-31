from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from djangoRLS.admin.RLSManagedModelAdmin import RLSManagedModelAdmin
from djangoRLS.models import RLSPermission
from djangoRLS.admin.models import RLSPermissionAdmin


admin.site.register(RLSPermission, RLSPermissionAdmin)
admin.site.register(ContentType)
