from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import smtplib, ssl
import getopt
import sys

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, '', ['date=', 'pass=', 'from=', 'to='])

day = date.today()
sender = receiver = email = ''

for (opt, value) in opts:
    if opt == "--date":
        day = value
    elif opt == "--pass":
        password = value
    elif opt == "--from":
        sender = value
    elif opt == "--to":
        receiver = value

if not sender or not receiver or not password:
    print("One or more required parameters empty")
    exit(1)

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

message = MIMEMultipart("alternative")
message["Subject"] = f"%s | HackerNews" % day
message["From"] = sender
message["To"] = receiver
message.attach(MIMEText(body, "html"))
context = ssl.create_default_context()
with smtplib.SMTP("smtp.mail.me.com", 587) as server:
    server.starttls(context=context)
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())
