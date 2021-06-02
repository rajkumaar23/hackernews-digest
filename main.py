from bs4 import BeautifulSoup
import requests

page = requests.get("https://news.ycombinator.com/front?day=2021-06-01")
soup = BeautifulSoup(page.content, 'html.parser')
items = soup.find_all('tr', class_="athing")[:10]
digest = []

for item in items:
    id = item['id']
    story = item.find('a', class_="storylink")
    title = story.text
    href = story['href']
    domain = getattr(item.find('span', class_="sitestr"), 'text', 'news.ycombinator.com')
    points = soup.find('span', id=("score_" + id)).text
    digest.append({
        'title': title,
        'href': href,
        'domain': domain,
        'points': points
    })

print(digest)