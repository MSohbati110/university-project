from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapeJob, ScrapedData
from .serializers import ScrapeJobSerializer, ScrapedDataSerializer
from .utils import scrape_url, scrape_selector_from_url

class ScrapeAPIView(APIView):
  def post(self, request):
    urls = request.data.get("urls", [])
    selectors = request.data.get("selectors", {})

    if not urls or not selectors:
      return Response({"error": "urls and selectors are required"}, status=status.HTTP_400_BAD_REQUEST)

    jobs = []
    for url in urls:
      job = ScrapeJob.objects.get_or_create(url=url)[0]

      if not job.html_content:
        job.html_content = scrape_url(url)
        job.save()

      data_list = scrape_selector_from_url(job, selectors)
      
      for item in data_list:
        ScrapedData.objects.get_or_create(
          job=job,
          element_name=item["element_name"],
          defaults={"element_value": item["element_value"]}
        )

      jobs.append(job)


    serializer = ScrapeJobSerializer(jobs, many=True)
    return Response(serializer.data)

class ScrapeJobsListAPIView(APIView): 
  def get(self, request):
    data = {}
    urls = ScrapeJob.objects.all().values_list('url', flat=True)

    for url in urls:
      unique_elements = ScrapedData.objects.filter(job__url=url).values_list('element_name', flat=True)
      data[url] = unique_elements

    return Response(data, status=status.HTTP_200_OK)

class ScrapeResultsAPIView(APIView):
  def post(self, request):
    url = request.data.get("url", None)
    selectors = request.data.get("selectors", None)

    results = ScrapedData.objects.filter(job__url=url, element_name__in=selectors)
    serilized_results = ScrapedDataSerializer(results, many=True)

    return Response(serilized_results.data, status=status.HTTP_200_OK)