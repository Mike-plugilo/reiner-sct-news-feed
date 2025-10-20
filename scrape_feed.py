import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.reiner-sct.com/news/"
OUTPUT_FILE = "rss.xml"

r = requests.get(URL)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

fg = FeedGenerator()
fg.title("REINER SCT News")
fg.link(href=URL)
fg.description("Automatisch generierter RSS-Feed")

for item in soup.select(".news__item"):
    title_elem = item.select_one(".news__item--title a")
    date_elem = item.select_one(".news__item--date")
    desc_elem = item.select_one(".news__item--text")
    
    if title_elem and date_elem:
        fe = fg.add_entry()
        fe.title(title_elem.text.strip())
        fe.link(href=title_elem["href"])
        fe.published(date_elem.text.strip())
        if desc_elem:
            fe.description(desc_elem.text.strip())

fg.rss_file(OUTPUT_FILE)
print(f"Feed erzeugt: {OUTPUT_FILE}")
