from django.urls import path
import account.views as views


urlpatterns = [    
    path('my_manuscripts', views.my_manuscripts, name='my_manuscripts'),
    path('all_manuscripts', views.all_manuscripts, name='all_manuscripts'),
    path('', views.my_login, name='account'),
    path('logout', views.my_logout, name='my_logout'),
    path('my_manuscripts/accept/<int:id>', views.accept, name='accept'),
    path('my_manuscripts/reject/<int:id>', views.reject, name='reject'),

]