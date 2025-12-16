from rest_framework import serializers
from .models import ScrapeJob, ScrapedData

class ScrapedDataSerializer(serializers.ModelSerializer):
  url = serializers.CharField(source='job.url', read_only=True)

  class Meta:
    model = ScrapedData
    fields = ['url', 'element_name', 'element_value']


class ScrapeJobSerializer(serializers.ModelSerializer):
  results = ScrapedDataSerializer(many=True, read_only=True)

  class Meta:
    model = ScrapeJob
    fields = ['id', 'url', 'results']
