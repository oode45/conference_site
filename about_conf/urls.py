from django.urls import path
from .views import conference_info


urlpatterns = [
    path('about', conference_info, {'template_name': 'about.html'}, name='about'),
    path('important_dates', conference_info, {'template_name': 'important_dates.html'}, name='important_dates'),
    path('contacts', conference_info, {'template_name': 'contacts.html'}, name='contacts'),
    path('orgcom', conference_info, {'template_name': 'orgcom.html'}, name='orgcom'),
    path('instructions', conference_info, {'template_name': 'instructions.html'}, name='instructions'),
    path('program', conference_info, {'template_name': 'program.html'}, name='program'),
]

