from django.urls import path
from web import views
from .views import *

#from django.contrib.auth import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('crawler/', views.crawler),
    path('divlist/', views.divlist),
    path('divlist/<int:divid>/result/', views.result),
    path('divlist/<int:divid>/result/delete/', views.delete),
    path('enddelete/', views.enddelete),
]