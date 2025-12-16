from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.ScrapeAPIView.as_view(), name='scrape'),
  path('jobs/', views.ScrapeJobsListAPIView.as_view(), name='scrape-jobs-list'),
  path('results/', views.ScrapeResultsAPIView.as_view(), name='scrape-results'),
]
