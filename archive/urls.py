from django.urls import path
from archive.views import archive_view


urlpatterns = [    
    path('', archive_view, name='archive'),

]