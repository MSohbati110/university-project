from django.urls import path, include
from . import views

urlpatterns = [
  path('scrape/', include("scraper.urls")),
]
