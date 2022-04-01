from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from djangoRLS.models import RLSPermission

USER_MODEL_CONTENT_TYPE = ContentType.objects.get_for_model(get_user_model())
GROUP_MODEL_CONTENT_TYPE = ContentType.objects.get_for_model(Group)


class RLSManagedModelAdmin(ModelAdmin):

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        permitted_ids = [record.record_object_id for record in RLSPermission.objects.filter(
            Q(
                (
                        Q(grantee_object_id=request.user.pk) &
                        Q(grantee_content_type=USER_MODEL_CONTENT_TYPE)
                ) |
                (
                        Q(grantee_object_id__in=list(request.user.groups.all().values_list('pk', flat=True))) &
                        Q(grantee_content_type=GROUP_MODEL_CONTENT_TYPE)
                )
            ),
            record_content_type=ContentType.objects.get_for_model(self.model)
        ).distinct()]

        return qs.filter(pk__in=permitted_ids)
