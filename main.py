
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

import requests
from bs4 import BeautifulSoup
import re



ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')

# извлекаем посты
posts = soup.find_all('article', class_='post')
#собираем ссылки на полные статьи
read_more_links = []
for post in posts:
    read_more_block = post.find_all('a', class_='btn btn_x-large btn_outline_blue post__habracut-btn')

    read_more_block = str(read_more_block)
    read_more_link = re.search("(https:\/\/habr\.com\/ru\/)(post|company)?\/?([\w]+)?\/?(blog)?\/?([\d]+)\/?#habracut", read_more_block).group(0)
    read_more_links.append(read_more_link)

#парсим тексты статей по ключевым словам
for link in read_more_links:

    ret = requests.get(link)
    soup = BeautifulSoup(ret.text, 'html.parser')

    article_text = soup.find('div', class_='post__body post__body_full')
    article_text = article_text.text


    if any([key_word in article_text for key_word in KEYWORDS]):

        title = soup.find('span', class_='post__title-text')
        title = title.text

        time_element = soup.find('span', class_='post__time')
        time_element = time_element.attrs.get('data-time_published')

        print(f'<{time_element}> - <{title}> - <{link}>')

