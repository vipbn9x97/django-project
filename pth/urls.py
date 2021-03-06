from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pth/output', views.getOutput),
    path('pth/dpmo', views.getDPMO),
    path('pth/error', views.getDefect)
]