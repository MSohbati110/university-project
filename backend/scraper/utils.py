import requests
from bs4 import BeautifulSoup

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
}

def scrape_url(url):
  response = requests.get(url, headers=headers ,timeout=10)
  response.raise_for_status()

  return response.text

def scrape_selector_from_url(job, selectors):
  if not job.html_content:
    return []

  soup = BeautifulSoup(job.html_content, 'html.parser')
  results = []

  for selector in selectors:
    # support CSS selectors
    elements = soup.select(selector)
    value = ", ".join([el.get_text(strip=True) for el in elements])
    results.append({
      "element_name": selector,
      "element_value": value
    })

  return results
