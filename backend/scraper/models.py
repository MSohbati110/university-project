from django.db import models

class ScrapeJob(models.Model):
  url = models.URLField(unique=True)
  html_content = models.JSONField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.url


class ScrapedData(models.Model):
  job = models.ForeignKey(ScrapeJob, on_delete=models.CASCADE, related_name="results")
  element_name = models.CharField(max_length=255)
  element_value = models.TextField()

  class Meta:
    unique_together = ("job", "element_name")  # prevents duplicate scraping for same element

  def __str__(self):
    return f"{self.element_name}: {self.element_value[:50]}"
