from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.sites import AlreadyRegistered

from djangoRLS.admin.filters import RLSManagedRelatedFieldListFilter
from djangoRLS.admin.models import RLSPermissionAdmin
from djangoRLS.admin.options import RLSManagedModelAdmin
from djangoRLS.models import RLSPermission

admin.site.register(RLSPermission, RLSPermissionAdmin)

try:
    admin.site.register(ContentType)
except AlreadyRegistered:
    pass
