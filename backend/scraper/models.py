from django.db import models

class ScrapeJob(models.Model):
  SOURCE_TYPE_CHOICES = (
    ("web", "Web Page"),
    ("api", "API"),
  )

  url = models.URLField(unique=True)
  source_type = models.CharField(
    max_length=10,
    choices=SOURCE_TYPE_CHOICES,
    default="web",
  )
  html_content = models.JSONField(blank=True, null=True)

  auto_scrape = models.BooleanField(default=False)
  scrape_interval = models.PositiveIntegerField(default=60)  # seconds
  last_scraped_at = models.DateTimeField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.source_type.upper()} - {self.url}"


class ScrapedData(models.Model):
  job = models.ForeignKey(ScrapeJob, on_delete=models.CASCADE, related_name="results")
  element_name = models.CharField(max_length=255)
  element_value = models.TextField()

  class Meta:
    unique_together = ("job", "element_name")  # prevents duplicate scraping for same element

  def __str__(self):
    return f"{self.element_name}: {self.element_value[:50]}"
