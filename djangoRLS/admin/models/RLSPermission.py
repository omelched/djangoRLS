from dal import autocomplete
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from djangoRLS.models import RLSPermission
from django.apps import apps

USER_MODEL = get_user_model()
RLSable_MODELS = [model for model in apps.get_models() if getattr(model._meta, 'RLSable', None)]


class RLSManagedModelAdminForm(autocomplete.FutureModelForm):
    class Meta:
        model = RLSPermission
        fields = (
            'record_ref',
            'grantee_ref',
        )

    record_ref = autocomplete.GenericForeignKeyModelField(
        model_choice=[(model,) for model in RLSable_MODELS],
        widget=autocomplete.QuerySetSequenceSelect2,
        view=autocomplete.Select2QuerySetSequenceView,
    )
    grantee_ref = autocomplete.GenericForeignKeyModelField(
        model_choice=[(USER_MODEL,), (Group,)],
        widget=autocomplete.QuerySetSequenceSelect2,
        view=autocomplete.Select2QuerySetSequenceView,
    )


class RLSPermissionAdmin(ModelAdmin):
    form = RLSManagedModelAdminForm
    list_display = ('record_ref', 'grantee_ref',)
    search_fields = ('reford_ref', 'grantee_ref',)
