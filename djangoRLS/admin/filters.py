from django.contrib.admin import RelatedFieldListFilter

from djangoRLS.admin.restrictions import apply_restrictions


class RLSManagedRelatedFieldListFilter(RelatedFieldListFilter):
    model = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.model = model

    def field_choices(self, field, request, model_admin):
        super_choices = super().field_choices(field, request, model_admin)

        qs = field.remote_field.model._default_manager.get_queryset()
        permitted_ids = tuple(apply_restrictions(qs, request.user).values_list('pk', flat=True))

        choices = tuple(
            super_choice
            for super_choice
            in super_choices
            if super_choice[0] in permitted_ids
        )

        return choices
