from django.urls import path
import participant_registration.views as views

urlpatterns = [
    path('', views.registration_captcha, name='registration_captcha'),
    path('form', views.registration_form, name='registration_form'),
    path('status', views.status_claim, name='status_claim'),
    path('inactive', views.registration_inactive, name='registration_inactive'),
    path('statistics', views.statistics, name='statistics'),
    path('agenda', views.agenda, name='agenda'),
]
