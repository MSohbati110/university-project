from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from .models import ScrapeJob, ScrapedData
from .serializers import ScrapeJobSerializer, ScrapedDataSerializer
from .utils import scrape_web, scrape_selector_from_web, scrape_api
from .scheduler import scheduler, auto_scrape_job

class ScrapeAPIView(APIView):
  def post(self, request):
    urls = request.data.get("urls", [])
    selectors = request.data.get("selectors", {})
    source_type = request.data.get("source_type", 'web')

    if not urls:
      return Response({"error": "urls are required"}, status=status.HTTP_400_BAD_REQUEST)
    if source_type == 'web' and not selectors:
      return Response({"error": "selectors are required"}, status=status.HTTP_400_BAD_REQUEST)

    jobs = []
    for url in urls:
      job = ScrapeJob.objects.get_or_create(url=url)[0]

      if source_type == 'web':
        if not job.html_content:
          job.source_type = 'web'
          job.html_content = scrape_web(url)
          job.last_scraped_at = timezone.now()
          job.save()

        data_list = scrape_selector_from_web(job, selectors)

        for item in data_list:
          ScrapedData.objects.get_or_create(
            job=job,
            element_name=item["element_name"],
            defaults={"element_value": item["element_value"]}
          )
      if source_type == 'api':
        if not job.html_content:
          job.source_type = 'api'
          job.html_content = scrape_api(url)
          job.last_scraped_at = timezone.now()
          job.save()

      jobs.append(job)

    serializer = ScrapeJobSerializer(jobs, many=True)
    return Response(serializer.data)

class ScrapeJobListAPIView(APIView):
  def get(self, request):
    jobs = ScrapeJob.objects.all().order_by("-created_at")
    data = [
      {
        "url": job.url,
        "auto_scrape": job.auto_scrape,
        "scrape_interval": job.scrape_interval,
        "last_scraped_at": job.last_scraped_at,
      }
      for job in jobs
    ]
    return Response(data)

class ScrapeSelectorsListAPIView(APIView): 
  def get(self, request):
    web_data = {}
    api_data = {}
    web_urls = ScrapeJob.objects.filter(source_type='web').values_list('url', flat=True)
    api_urls = ScrapeJob.objects.filter(source_type='api').values_list('url', flat=True)

    for url in web_urls:
      unique_elements = ScrapedData.objects.filter(job__url=url).values_list('element_name', flat=True)
      web_data[url] = unique_elements
    for url in api_urls:
      unique_elements = ScrapedData.objects.filter(job__url=url).values_list('element_name', flat=True)
      api_data[url] = unique_elements

    data = {
      'web': web_data,
      'api': api_data
    }

    return Response(data, status=status.HTTP_200_OK)

class ScrapeResultsAPIView(APIView):
  def post(self, request):
    url = request.data.get("url", None)
    selectors = request.data.get("selectors", None)
    source_type = request.data.get("source_type", 'web')

    if source_type == 'web':
      results = ScrapedData.objects.filter(job__url=url, element_name__in=selectors)
      serilized_results = ScrapedDataSerializer(results, many=True)
      return Response(serilized_results.data, status=status.HTTP_200_OK)
    if source_type == 'api':
      results = ScrapeJob.objects.filter(url=url)[0]
      return Response(results.html_content, status=status.HTTP_200_OK)

class ToggleAutoScrapeAPIView(APIView):
  def post(self, request):
    url = request.data.get("url")
    enabled = request.data.get("enabled", False)

    job = ScrapeJob.objects.get(url=url)
    job.auto_scrape = enabled
    job.save()

    job_id = f"auto_scrape_{job.id}"

    if enabled:
      scheduler.add_job(
        auto_scrape_job,
        "interval",
        seconds=job.scrape_interval,
        args=[url],
        id=job_id,
        replace_existing=True,
      )
    else:
      if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    return Response({"auto_scrape": enabled})
