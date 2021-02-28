from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):

    def short_content(self, obj):
        return obj.content

    short_content.short_description = u'Текст'

    fields = [
        'title',
        'content',
        'posting_date',
        'thumbnail_image',
        'image1',
        'image2',
        'image3'
    ]
    list_display = ['posting_date', 'title', 'short_content']
    ordering = ['-posting_date', 'title']
    search_field = ['content']


admin.site.register(News, NewsAdmin)
