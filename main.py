from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from datetime import date
import requests
import getopt
import sys

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, '', ['date='])

day = date.today()
for (opt, value) in opts:
    if opt == "--date":
        day = value

page = requests.get("https://news.ycombinator.com/front?day=" + day)
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

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('newsletter.jinja')
body = template.render(day=day, digest=digest)