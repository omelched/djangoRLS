from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, QuerySet

from djangoRLS.models import RLSPermission

USER_MODEL_CONTENT_TYPE = ContentType.objects.get_for_model(get_user_model())
GROUP_MODEL_CONTENT_TYPE = ContentType.objects.get_for_model(Group)


def apply_restrictions(qs: QuerySet, user):
    if user.is_superuser:
        return qs

    if RLSPermission.objects.filter(
            Q(
                (
                        Q(grantee_object_id=user.pk) &
                        Q(grantee_content_type=USER_MODEL_CONTENT_TYPE)
                ) |
                (
                        Q(grantee_object_id__in=list(user.groups.all().values_list('pk', flat=True))) &
                        Q(grantee_content_type=GROUP_MODEL_CONTENT_TYPE)
                )
            ),
            record_content_type=ContentType.objects.get_for_model(qs.model),
            permit_all=True,
    ).exists():
        return qs

    permitted_ids = [record.record_object_id for record in RLSPermission.objects.filter(
        Q(
            (
                    Q(grantee_object_id=user.pk) &
                    Q(grantee_content_type=USER_MODEL_CONTENT_TYPE)
            ) |
            (
                    Q(grantee_object_id__in=list(user.groups.all().values_list('pk', flat=True))) &
                    Q(grantee_content_type=GROUP_MODEL_CONTENT_TYPE)
            )
        ),
        record_content_type=ContentType.objects.get_for_model(qs.model)
    ).distinct()]

    return qs.filter(pk__in=permitted_ids)
