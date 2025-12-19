from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import ScrapeJob, ScrapedData
from .utils import scrape_web, scrape_selector_from_web

scheduler = BackgroundScheduler()

def auto_scrape_job(job_url):
  job = ScrapeJob.objects.filter(url=job_url).first()

  if not job:
    print(f"[Scheduler] Job not found, skipping: {job_url}")
    return
  if not job.auto_scrape:
    return

  job.html_content = scrape_web(job_url)
  job.save()

  selectors = ScrapedData.objects.filter(job__url=job_url).values_list('element_name', flat=True)
  data_list = scrape_selector_from_web(job, selectors)

  for item in data_list:
    data = ScrapedData.objects.get(
      job=job,
      element_name=item["element_name"]
    )
    data.element_value = item["element_value"]
    data.save()

  job.last_scraped_at = timezone.now()
  job.save()
