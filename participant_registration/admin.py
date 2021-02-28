from django.contrib import admin

# Register your models here.
from .models import Country, Section, Participant, RegistrationStatus


class ParticipantAdmin(admin.ModelAdmin):

    def short_content(self, obj):
        return obj.__str__()

    def registration_year(self, obj):
        return obj.registration_date.year

    short_content.short_description = u'Описание'
    registration_year.short_description = u'Год'

    fields = [
        'last_name',
        'first_name',
        'middle_name',
        'age',
        'country',
        'current_status',
        'phone',
        'email',
        'organization',
        'section',
        'participation_type',
        'author_list',
        'paper_name',
        'paper_file',
        'chief_last_name',
        'chief_first_name',
        'chief_middle_name',
        'chief_phone',
        'chief_email',
        'chief_organization',
        'chief_position',
        'chief_degree',
        'chief_review',
        'status_type',
        'reviewer',
        'reviewer_corrected_manuscript_pdf',
        'reviewer_corrected_manuscript',
        ]

    list_display = ['registration_year', 'section', 'short_content', 'id', 'reviewer', 'email', 'status_type', 'paper_name', 'participation_type', 'registration_date','reviewer_corrected_manuscript','reviewer_corrected_manuscript_pdf']
    list_display_links = ['short_content']
    registration_year.admin_order_field = 'registration_year'
    ordering = ['section', 'last_name']
    list_filter = ['status_type']
    search_fields = ['last_name']


class RegistrationStatusAdmin(admin.ModelAdmin):
    fields = ['is_active', 'registration_inactive_text']
    list_display = ['is_active', 'registration_inactive_text']


admin.site.register(Country)
admin.site.register(Section)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(RegistrationStatus, RegistrationStatusAdmin)
