import logging
import re
from bs4 import BeautifulSoup
import requests, json

logger = logging.getLogger(__name__)

''' парсер для считывания данных с сайта kassy.ru '''
def created_mailing_list():
    headers = {
        'Accept': '*/*',
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.84 Safari/537.36 '
    }
    i = 0
    urls_data = {'content' + str(i): []}
    urls = []
    with open('json_url.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        for url_all_banner in file['url']:
            urls.append(url_all_banner['banner_url'])
            urls_data['content' + str(i)].append({'banner_url': url_all_banner['banner_url']})

    for url in urls:
        req = requests.get(url, headers=headers)
        with open('parser.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

        with open('parser.html', encoding='utf-8') as file:
            src = file.read()
            soup = BeautifulSoup(src, 'xml')

        try:
            name_event = soup.find(class_='content').find('h1').find('a').string.lower()
        except Exception:
            name_event = 'Не нашли названия'
        try:
            rate = soup.find(class_='RARS').string
        except Exception:
            rate = 'нет ценза'
        try:
            date_event_all = soup.find(class_='venue').text.split('\n')[0].split()
            date_event = ''.join(date_event_all[:-2])
            time_event = ''.join(date_event_all[3:4])
        except Exception:
            date_event = 'не нашли дату'
            time_event = 'не нашли время'
        try:
            venue = soup.find(class_='venue').find('a').string
        except Exception:
            venue = 'не нашли место'
        try:
            price = soup.find(class_='price').find('p').text.split(':')[1].replace('', '')
        except Exception:
            price = 'не нашли цену'
        try:
            number_phone_liks = soup.find(id='city_phone').get('href')
            number_phone = soup.find(id='city_phone').text
        except Exception:
            number_phone = 'не нашли телефон'
            number_phone_liks = 'не нашли ссылку на телефон'
        try:
            alert_date = soup.find(class_='message alert-danger').text
        except Exception:
            alert_date = 'Нет времени переноса'

        reg = r"^()?()()([\w\-\.]+[^#?\d]+)(.*)\/$"
        reg_ts = r"\d+(?=-(?!-))"
        reg_id = r"\d+$(?!-(?=-))"
        label = re.search(reg, url).group(5)
        ts_ud = re.search(reg_ts, label)
        id = re.search(reg_id, label)
        labels = '__' + label

        urls_data['content' + str(i)].append({
            'name_event': name_event,
            'rate': rate,
            'date_event': date_event,
            'time_event': time_event,
            'venue': venue,
            'price': price,
            'number_phone_liks': number_phone_liks,
            'number_phone': number_phone,
            'alert_date': alert_date,
            'labels': labels,
        })
        i += 1

    with open('json_content.json', 'w', encoding='utf8') as file:
        json.dump(urls_data, file, indent=4)


''' распаковываем json в словарь для передачи в контекст '''
def unpack(context):
    with open('json_content.json', 'r', encoding='utf8') as file:
        file = json.load(file)
        for date in file['content']:
            context.update(date['transfer'])
            context.update(date['transfer_date'])
    with open('json_url.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        for url in file['url']:
            context.update(url)
    return context


def unpuck_banner(context):
    with open('json_content.json', 'r', encoding='utf8') as file:
        file = json.load(file)
        for date in file['content']:
            context.update(date['banner_date'])
            context.update(date['banner_title_content'])
            context.update(date['banner_content'])
    with open('json_url.json', 'r', encoding='utf-8') as file:
        file = json.load(file)
        for url in file['url']:
            context.update(url)
    return context

