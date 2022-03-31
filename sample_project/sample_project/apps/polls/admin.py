from django.contrib import admin

from .models import Choice, Question, Tags

from djangoRLS.admin import RLSManagedModelAdmin


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(RLSManagedModelAdmin):
    fieldsets = [
        (
            None,
            {
                'fields': ('question_text',)
            }
        ),
        (
            'Date information',
            {
                'fields': ('pub_date',),
                'classes': ('collapse',)
            }
        ),
        (
            'Other info',
            {
                'fields': ('tags',),
                # 'classes': ('collapse',)
            }
        ),
    ]
    inlines = [ChoiceInline, ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)
    filter_horizontal = ('tags',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Tags, admin.ModelAdmin)
