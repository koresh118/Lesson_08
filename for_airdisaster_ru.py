# Импортируем необходимые библиотеки и модули
import requests
import csv
from pprint import pprint
from lxml.html import fromstring
from datetime import date
from pymongo import MongoClient


# Создаём класс "Авиапроисшествие"
class Airdisaster():

    def __init__(self, dom, link_disaster):
        self.dom = dom
        self.link = link_disaster
        tittle = ''
        total_number_of_deaths = ''

    def run_parse(self):
        Airdisaster.get_tittle(self)
        Airdisaster.get_deaths(self)
        Airdisaster.get_brief_characteristics(self, self.link, self.tittle, self.total_number_of_deaths)

        Airdisaster.get_characteristics(self, self.params, self.brief_characteristics)
        print(self.characteristics)
        Airdisaster.add_data(self, self.characteristics)

    def get_tittle(self):
        tittle = dom.xpath("//span[@class='txt14']//text()")
        tittle = tittle[0]
        setattr(self, 'tittle', tittle)

    def get_brief_characteristics(self, link, tittle, total_number_of_deaths):
        description = dom.xpath("//div[@class='txt16']/text()")
        description = description[0]
        brief_characteristics = dom.xpath("//b/../text()")  # "//b/text()")

        brief_characteristics.append(description)
        for param in brief_characteristics:
            if (param == '\n'):
                brief_characteristics.remove(param)
        brief_characteristics = [sub.replace('\xa0\xa0', '') for sub in brief_characteristics]
        brief_characteristics.insert(0, tittle)
        brief_characteristics.insert(0, link)
        params = dom.xpath('//b/text()')
        params.insert(0, 'Наименование')
        params.insert(0, 'Ссылка')
        params.insert((len(params) - 1), 'Всего погибших')
        brief_characteristics.insert((len(params) - 2), total_number_of_deaths)
        setattr(self, 'params', params)
        setattr(self, 'brief_characteristics', brief_characteristics)

    def get_deaths(self):
        total_number_of_deaths = dom.xpath('//td[text()="Всего погибших"]/..//b/font/text()')
        total_number_of_deaths = total_number_of_deaths[0]
        setattr(self, 'total_number_of_deaths', total_number_of_deaths)

    def get_characteristics(self, params, brief_characteristics):
        characteristics = dict(zip(params, brief_characteristics))
        setattr(self, 'characteristics', characteristics)

    def add_data(self, characteristics):
        airdisasters.insert_one(characteristics)


# Назначаем параметры для работы с MongoDB
MONGO_HOST = "localhost"
MONGO_PORT = 27017
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.airdisaster_ru
airdisasters = db.airdisasters

# Основные параметры запроса
url = 'http://www.airdisaster.ru/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36"
}

# Запрос исходного кода страницы
response_1 = requests.get(url, headers=headers)
dom_1 = fromstring(response_1.text)

# Основной код программы
link_list = dom_1.xpath("//a[@class='xt04']/@href")
for i in range(len(link_list)):
    link_year = 'http://www.airdisaster.ru' + link_list[i]
    response_2 = requests.get(link_year, headers=headers)
    dom_2 = fromstring(response_2.text)
    links_disasters = dom_1.xpath("//td[@class='tdh2']/a/@href")
    for i in range(len(links_disasters)):
        link_disaster = 'http://www.airdisaster.ru' + links_disasters[i]
        response = requests.get(link_disaster, headers=headers)
        dom = fromstring(response.text)
        link__ = Airdisaster(dom, link_disaster)
        link__.run_parse()

