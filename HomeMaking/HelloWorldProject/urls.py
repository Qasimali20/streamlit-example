from django.urls import path
from helloworldapp import views
from django.contrib import admin
from django.views.generic import TemplateView

from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('cv/', views.page, name='cv'),
    ]

