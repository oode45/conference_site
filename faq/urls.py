from django.urls import path
from faq.views import faq_view


urlpatterns = [    
    path('', faq_view, name='faq'),

]