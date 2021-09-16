import requests
import re
from bs4 import BeautifulSoup

KEYWORDS = {'дизайн', 'фото', 'web', 'Python'}
URL = 'https://habr.com'
response = requests.get('https://habr.com/ru/all/')
response.raise_for_status()
soup = BeautifulSoup(response.text, features='html.parser')

articles = soup.find_all('article')
for article in articles:
    titles = article.find_all('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2')
    title_list = []
    for title in titles:
        title_list.extend(re.split('; |, |\* |\. | |\?|\.|-|\(|\)|:',title.text))
        title_set = set(title_list)
    hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
    hub_list = []
    for hub in hubs:
        hub_list.extend(re.split('; |, |\* |\. | |\?|\.|-|\(|\)|:',hub.text))
        hub_set = set(hub_list)
    bodys = article.find_all('div', class_='article-formatted-body article-formatted-body_version-2')
    body_list = []
    for body in bodys:
        body_list.extend(re.split('; |, |\* |\. | |\?|\.|-|\(|\)|:', body.text))
        body_set = set(body_list)
    if KEYWORDS & title_set | KEYWORDS & hub_set | KEYWORDS & body_set:
        date_ = article.find('time').attrs.get('title')
        title = article.find('h2')
        href = title.find('a').attrs.get('href')
        print(date_, title.text, URL + href)