from django.contrib import admin
from .models import Archive
from .models import File


class ArchiveAdminInline(admin.TabularInline):
    model = File
    extra = 1


class ArchiveAdmin(admin.ModelAdmin):
    inlines = [ArchiveAdminInline, ]


admin.site.register(Archive, ArchiveAdmin)
