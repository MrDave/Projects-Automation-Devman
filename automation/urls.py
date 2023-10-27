from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('students', views.students, name='students'),
    path('pms', views.pms, name='pms'),
    path('info_pro', views.info_pro, name='info'),
]