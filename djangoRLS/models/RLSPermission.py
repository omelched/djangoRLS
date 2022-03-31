from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class RLSPermission(models.Model):
    class Meta:
        verbose_name = _('Record Level Security permission')
        verbose_name_plural = _('Record Level Security permissions')
        constraints = [
            models.UniqueConstraint(fields=['record_content_type', 'record_object_id',
                                            'grantee_content_type', 'grantee_object_id'],
                                    name='unique record and grantee')
        ]

    record_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='rls_permissions',
        null=False,
        blank=False,
        verbose_name=_('record content type'),
    )
    record_object_id = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        verbose_name=_('object id'),
    )
    record_ref = GenericForeignKey(
        'record_content_type',
        'record_object_id'
    )
    grantee_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='rls_permitted',
        null=False,
        blank=False,
        verbose_name=_('grantee content type'),
    )
    grantee_object_id = models.CharField(
        max_length=36,
        null=False,
        blank=False,
        verbose_name=_('grantee id'),
    )
    grantee_ref = GenericForeignKey(
        'grantee_content_type',
        'grantee_object_id'
    )
