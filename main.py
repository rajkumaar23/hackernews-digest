from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlparse
import requests
import smtplib, ssl
import getopt
import sys

def is_absolute(url):
    return bool(urlparse(url).netloc)

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, '', ['date=', 'pass=', 'from=', 'to=', 'host='])

day = date.today()
sender = receiver = email = host = ''

for (opt, value) in opts:
    if opt == "--date":
        day = value
    elif opt == "--pass":
        password = value
    elif opt == "--from":
        sender = value
    elif opt == "--to":
        receiver = value
    elif opt == "--host":
        host = value

if not sender or not receiver or not password or not host:
    print("One or more required parameters empty")
    exit(1)

page = requests.get("https://news.ycombinator.com/front?day=" + day)
soup = BeautifulSoup(page.content, 'html.parser')
items = soup.find_all('tr', class_="athing")[:10]
print("10 items fetched")

digest = []
print("Processing each story")
for item in items:
    id = item['id']
    story = item.find('a', class_="titlelink")
    title = story.text
    href = story['href']
    domain_item = item.find('span', class_="sitestr")
    if domain_item:
        domain = domain_item.text
    else:
        domain = 'news.ycombinator.com'
    href = href if is_absolute(href) else 'https://' + domain + '/' + (href.strip("/"))
    points = soup.find('span', id=("score_" + id)).text
    digest.append({
        'title': title,
        'href': href,
        'domain': domain,
        'points': points
    })
    print("Processed story with id = " + id)

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('newsletter.jinja')
body = template.render(day=day, digest=digest)
print("Preparing digest email body")

message = MIMEMultipart("alternative")
message["Subject"] = f"%s | HackerNews" % day
message["From"] = sender
message["To"] = receiver
message.attach(MIMEText(body, "html"))
context = ssl.create_default_context()
with smtplib.SMTP(host, 587) as server:
    server.starttls(context=context)
    print("Loggin in via SMTP")
    res = server.login(sender, password)
    print(res)
    server.sendmail(sender, receiver, message.as_string())
    print("Email sent")
