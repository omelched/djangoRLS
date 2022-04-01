from django.contrib.admin import ModelAdmin
from django.db.models.fields.related import RelatedField

from djangoRLS.admin.restrictions import apply_restrictions
from djangoRLS.admin import RLSManagedRelatedFieldListFilter


class RLSManagedModelAdmin(ModelAdmin):
    related_RLSManaged_fields = ()

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        if not self.related_RLSManaged_fields:
            self.related_RLSManaged_fields = tuple(
                field for field in self.model._meta.fields
                if isinstance(field, RelatedField) and getattr(field.remote_field.model._meta, 'RLSable', None)
            )

    def get_field_queryset(self, db, db_field, request):
        qs = super().get_field_queryset(db, db_field, request)
        model = db_field.remote_field.model

        if getattr(model._meta, 'RLSable', None):
            return apply_restrictions(qs, request.user)
        else:
            return qs

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if getattr(self.model, 'RLSable', None):
            return apply_restrictions(qs, request.user)

        RLSable_related_filter = {
            f'{field.name}__in': self.get_field_queryset(None, field, request)
            for field in self.related_RLSManaged_fields
        }

        return qs.filter(**RLSable_related_filter)

    def get_list_filter(self, request):
        super_list_filter = super().get_list_filter(request)
        new_list_filter = []

        for filter_item in super_list_filter:
            if isinstance(filter_item, type):
                new_list_filter.append(filter_item)
                continue

            if isinstance(filter_item, tuple):
                if isinstance(filter_item[-1], type):
                    new_list_filter.append(filter_item)
                    continue

                if filter_item[1].startswith(tuple(field.name for field in self.related_RLSManaged_fields)):
                    new_list_filter.append(
                        (
                            filter_item[1], RLSManagedRelatedFieldListFilter,
                        )
                    )
                    continue

            if filter_item.startswith(tuple(field.name for field in self.related_RLSManaged_fields)):
                new_list_filter.append(
                    (
                        filter_item, RLSManagedRelatedFieldListFilter,
                    )
                )
                continue

            new_list_filter.append(
                filter_item
            )

        return new_list_filter
