from pprint import pprint
from lxml import html
import requests
import datetime
import timestring

import unidecode
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

# обрабатываем Лента.ру
lenta_url = 'https://lenta.ru'
response_lenta = requests.get(lenta_url, headers=header)
dom_lenta = html.fromstring(response_lenta.text)

lenta_news = []
items = dom_lenta.xpath("//div[@class='first-item']")
for item in items:
    lenta_item = {}
    name = item.xpath('./h2/a/text()')
    time = item.xpath('.//a/time/@datetime')
    link = item.xpath('./h2/a/@href')
    source = 'lenta.ru'

    lenta_item['name'] = ((' '.join(name).replace('\xa0',' ')))

    lenta_item['time'] = time[0]
    lenta_item['link'] = lenta_url+link[0]
    lenta_item['source'] = source
    lenta_news.append(lenta_item)

items = dom_lenta.xpath("//div[@class='item']")

for item in items:
    lenta_item = {}
    name = item.xpath('.//a/text()')
    time = item.xpath('.//a/time/@datetime')
    link = item.xpath('.//a/@href')
    source = 'lenta.ru'

    lenta_item['name'] = ((' '.join(name).replace('\xa0',' ')))
    if time !=[]:
       lenta_item['time'] = time[0]
    else:
       lenta_item['time'] = str(datetime.date.today())
    lenta_item['link'] = lenta_url+link[0]
    lenta_item['source'] = source
    lenta_news.append(lenta_item)
pprint(lenta_news)

# обрабатываем yandex.news
yandex_url = "https://yandex.ru/news/"
response_yandex = requests.get(yandex_url, headers=header)
dom_yandex = html.fromstring(response_yandex.text)
yandex_news = []

# сначала обрабатываем главную картинку
items = dom_yandex.xpath("//article[@class='mg-card mg-card_type_image mg-card_flexible-double mg-grid__item']")
for item in items:
    yandex_item = {}
    name = item.xpath('.//h2[@class="mg-card__title"]/text()')
    time = item.xpath('.//span[@class="mg-card-source__time"]/text()')
    link = item.xpath('.//a[@class="mg-card__link"]/@href')

    source = item.xpath('.//a[@class="mg-card__source-link"]/text()')

    yandex_item['name'] = (((' '.join(name)).replace('\xa0',' ')))
    #if time !=[]:
    #    lenta_item['time'] = str(datetime.date.today()) +' '+ time[0]
   #else:
       # lenta_item['time'] = str(datetime.date.today())
    yandex_item['time'] =str(datetime.date.today()) +' ' + ' '.join(time)
    yandex_item['link'] = link
    yandex_item['source'] = ' '.join(source)
    yandex_news.append(yandex_item)
#потом обрабатываем блоки с новостями поменьше
items = dom_yandex.xpath("//article[@class='mg-card mg-card_flexible-single mg-card_type_image mg-grid__item']")

for item in items:
    yandex_item = {}
    name = item.xpath('.//h2[@class="mg-card__title"]/text()')
    #time = item.xpath('.//a[@class="mg-card-source__time"]/text()')
    #link = item.xpath('.//span[@class="mg-card-source__time"]/text()')
    time = item.xpath('.//span[@class="mg-card-source__time"]/text()')
    link = item.xpath('.//a[@class="mg-card__source-link"]/@href')

    source = item.xpath('.//a[@class="mg-card__source-link"]/text()')

    yandex_item['name'] = (((' '.join(name)).replace('\xa0',' ')))
    #if time !=[]:
    #    lenta_item['time'] = str(datetime.date.today()) +' '+ time[0]
   #else:
       # lenta_item['time'] = str(datetime.date.today())
    yandex_item['time'] =str(datetime.date.today()) +' ' + ' '.join(time)
    yandex_item['link'] = link
    yandex_item['source'] = ' '.join(source)
    yandex_news.append(yandex_item)
pprint(yandex_news)


# обрабатываем mail.ru

mail_url = "https://news.mail.ru/"
response_mail = requests.get(mail_url, headers=header)
dom_mail = html.fromstring(response_mail.text)

# сначала обрабатываем главную новость дня
items_mail=dom_mail.xpath("//div[@class='daynews__item daynews__item_big']")
mail_news = []
for item in items_mail:
    mail_item = {}


    name = item.xpath('.//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text()')
    time = datetime.date.today()
    link = item.xpath('.//a[@class="photo photo_full photo_scale js-topnews__item"]/@href')

    mail_item['name'] = (((' '.join(name)).replace('\xa0',' ')))
    #if time !=[]:
    #    lenta_item['time'] = str(datetime.date.today()) +' '+ time[0]
   #else:
       # lenta_item['time'] = str(datetime.date.today())
    mail_item['time'] =time
    mail_item['link'] = link
    mail_item['source'] = 'Mail.ru'
    mail_news.append(mail_item)

# обрабатываем новости на картинках
items_mail=dom_mail.xpath("//div[@class='daynews__item']")

for item in items_mail:
    mail_item = {}


    name = item.xpath('.//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/text()')
    time = datetime.date.today()
    link = item.xpath('.//a[@class="photo photo_small photo_scale photo_full js-topnews__item"]/@href')

    mail_item['name'] = (((' '.join(name)).replace('\xa0',' ')))
    #if time !=[]:
    #    lenta_item['time'] = str(datetime.date.today()) +' '+ time[0]
   #else:
       # lenta_item['time'] = str(datetime.date.today())
    mail_item['time'] =time
    mail_item['link'] = link
    mail_item['source'] = 'Mail.ru'
    mail_news.append(mail_item)

items_mail=dom_mail.xpath("//ul[@class='list list_type_square list_half js-module']//li[@class='list__item']")

for item in items_mail:
    mail_item = {}
    name = item.xpath('.//a[@class="list__text"]/text()')
    time = datetime.date.today()
    link = item.xpath('.//a[@class="list__text"]/@href')

    mail_item['name'] = (((' '.join(name)).replace('\xa0',' ')))
    #if time !=[]:
    #    lenta_item['time'] = str(datetime.date.today()) +' '+ time[0]
   #else:
       # lenta_item['time'] = str(datetime.date.today())
    mail_item['time'] =time
    mail_item['link'] = link
    mail_item['source'] = 'Mail.ru'
    mail_news.append(mail_item)


pprint(mail_news)