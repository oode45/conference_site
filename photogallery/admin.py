from django.contrib import admin
from .models import Gallery
from .models import Images


class GalleryImageInline(admin.TabularInline):
    model = Images
    extra = 2


class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline, ]


admin.site.register(Gallery, GalleryAdmin)
