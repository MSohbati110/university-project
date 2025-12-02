from django.urls import path, include
from . import views

urlpatterns = [
  path('example', views.Example.as_view(), name='example'),
]
