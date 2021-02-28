from django.contrib import admin
from .models import Conference
from django.utils.safestring import mark_safe
import markdown


class ConferenceAdmin(admin.ModelAdmin):

    def short_important_dates(self, obj):
        return mark_safe(markdown.markdown(obj.important_dates))

    def short_about(self, obj):
        return mark_safe(markdown.markdown(obj.about))

    def short_contacts(self, obj):
        return mark_safe(markdown.markdown(obj.contacts))

    def short_academic_secretary_info(self, obj):
        return mark_safe(markdown.markdown(obj.academic_secretary_info))

    def short_instructions(self, obj):
        return mark_safe(markdown.markdown(obj.instructions))

    def short_chairman_info(self, obj):
        return mark_safe(markdown.markdown(obj.chairman_info))

    def short_committee_members(self, obj):
        return mark_safe(markdown.markdown(obj.committee_members))

    short_about.short_description = u'О конференции'
    short_important_dates.short_description = u'Важные даты'
    short_contacts.short_description = u'Контакты'
    short_academic_secretary_info.short_description = u'Данные секретаря'
    short_instructions.short_description = u'Требования к оформлению'
    short_chairman_info.short_description = u'Данные председателя'
    short_committee_members.short_description = u'Данные участников оргкомитета'

    fields = [
        'important_dates',
        'about',
        'contacts',
        'academic_secretary_info',
        'instructions',
        'chairman_info',
        'committee_members',
        'image_station',
        'map_image',
        'academic_secretary_image',
        'map_source_name1',
        'map_source_url1',
        'map_source_name2',
        'map_source_url2',
        'instructions_file',
        'pattern_file',
        'chairman_photo',
        'comment_accepted',
        'comment_rejected',
    ]

    list_display = ['short_academic_secretary_info', 'short_chairman_info', 'short_important_dates']


admin.site.register(Conference, ConferenceAdmin)
