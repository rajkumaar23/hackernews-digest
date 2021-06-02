from bs4 import BeautifulSoup
from datetime import date
import requests
import getopt
import sys

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, '', ['date='])

today = date.today()
for (opt, value) in opts:
    if opt == "--date":
        today = value

page = requests.get("https://news.ycombinator.com/front?day=" + today)
soup = BeautifulSoup(page.content, 'html.parser')
items = soup.find_all('tr', class_="athing")[:10]
digest = []

for item in items:
    id = item['id']
    story = item.find('a', class_="storylink")
    title = story.text
    href = story['href']
    domain_item = item.find('span', class_="sitestr")
    if domain_item:
        domain = domain_item.text
    else:
        domain = 'news.ycombinator.com'
    points = soup.find('span', id=("score_" + id)).text
    digest.append({
        'title': title,
        'href': href,
        'domain': domain,
        'points': points
    })

print(digest)