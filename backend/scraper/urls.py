from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.ScrapeAPIView.as_view(), name='scrape'),
  path('selectors/', views.ScrapeSelectorsListAPIView.as_view(), name='scrape-selectors-list'),
  path('jobs/', views.ScrapeJobListAPIView.as_view(), name='scrape-jobs-list'),
  path('results/', views.ScrapeResultsAPIView.as_view(), name='scrape-results'),
  path('jobs/toggle/', views.ToggleAutoScrapeAPIView.as_view(), name='scrape-jobs-automate'),
]
