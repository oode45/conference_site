"""conference_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.news_list, name='home'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('registration/', include('participant_registration.urls'), name='registration'),
    path('archive/', include('archive.urls')),
    path('photogallery/', include('photogallery.urls')),
    path('faq/', include('faq.urls')),
    path('conference/', include('about_conf.urls')),
    path('account/', include('account.urls')),
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Сайт молодежной конференции'
