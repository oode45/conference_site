from django.contrib import admin
from .models import Faq


class FaqAdmin(admin.ModelAdmin):

    fields = [
        'order',
        'question',
        'answer',
        'helper_image',
        'helper_file'
    ]
    list_display = ['question', 'answer']
    # ordering = ['order', 'question']
    # search_field = ['question']


admin.site.register(Faq, FaqAdmin)

# Register your models here.
