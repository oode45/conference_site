from django.urls import path
from photogallery.views import photogallery_view


urlpatterns = [    
    path('', photogallery_view, name='photogallery'),

]