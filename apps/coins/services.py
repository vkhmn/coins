#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from datetime import datetime
import re
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time
from functools import reduce

from apps.coins.models import Seller


class Coin:   
    __ROOT_URL = 'https://coins.lave.ru/forum'

    def __init__(self, category, header, coin_id, title, img_url, user, end_date):
        self.__header = header
        self.__category_object = category
        self.__category = category.id
        self.__id = coin_id
        self.__title = title
        self.__img_url = img_url
        self.__user = user
        self.__end_date = end_date

    @property
    def img_url(self):
        return self.__img_url

    @img_url.setter
    def img_url(self, value):
        self.__img_url = value

    @property
    def coin_url(self):
        return f'{self.__ROOT_URL}/viewtopic.php?f={self.__category}&t={self.__id}'

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    @property
    def coin_id(self):
        return self.__id

    def to_db(self):
        seller, _ = Seller.objects.get_or_create(name=self.__user)
        return dict(
            id=self.__id,
            category=self.__category_object,
            title=self.__title,
            image=self.__img_url,
            seller=seller,
            end_date=datetime.today()  # self.__end_date,
        )

    def to_msg(self):
        return f'*{self.__header}*\n' \
               f'{self.__title}\n' \
               f'{self.__user}\n' \
               f'{self.coin_url}', self.img_url


class CoinsCollect:

    __ROOT_URL = 'https://coins.lave.ru/forum'

    OLD_DATE = False
    IS_UNC = True

    def __init__(self, category=None, pattern=None):        
        self.init(category, pattern)
        self.__coins = []
        self.__header = None

    def init(self, category, pattern):
        self.__pattern = pattern
        if category:
            self.__category_object = category
            self.__category = category.id
            self.__url = f'https://coins.lave.ru/forum/viewforum.php?f={category.id}'

    def __page_url(self, page):
        return f'{self.__url}&start={page}'

    @property
    def coins(self):
        return self.__coins

    async def __get_img(self, session, coin: Coin):
        async with session.get(url=coin.coin_url) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            img_in = soup.find('img', src=re.compile(r'thumb\/'))
            img_out = soup.find('img', alt='Изображение')
            img = img_in or img_out or None
            if img:
                coin.img_url = img.get('src', None)
        return coin

    async def __get_page_data(self, session, page_url):
        async with session.get(url=page_url) as response:
            tasks = []
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            tds = soup.find_all('a', class_="topictitle")
            for td in tds:
                title = td.text.strip()
                desc = td.get('title')
                date = __class__.__find_date(title + desc)
                searching = bool(re.search(self.__pattern, title))
                is_unc = bool(re.search(u'unc|унц|блеск|штемп|без обращ|мешков', (title + desc).lower()))
                old_date = __class__.__is_old_date(date)
                if searching and (is_unc and self.IS_UNC) and (not old_date or self.OLD_DATE):
                    coin_id = td.get('href').split('=')[-1]
                    user = td.find_parent('tr').find('p', class_="topicauthor").text.strip()
                    params = {
                            'category': self.__category_object,
                            'header': self.__header,
                            'coin_id': int(coin_id),
                            'title': title,
                            'img_url': None,
                            'user': user,
                            'end_date': int(date.timestamp()),
                            }
                    coin = Coin(**params)
                    tasks += [asyncio.create_task(self.__get_img(session, coin))]
        return tasks

    async def __gather_data(self):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=self.__url)
            soup = BeautifulSoup(await response.text(), 'lxml')
            page_urls = soup.find('td', class_="gensmall", align="right").find_all('a')
            pages_count = int(page_urls[-2].text) if page_urls else 1
            self.__header = soup.find('div', id="pageheader").text.strip().split('\n')[0]
            
            tasks = []
            for index in range(0, (pages_count - 1) * 50 + 1, 50):
                task = asyncio.create_task(self.__get_page_data(session, self.__page_url(index)))
                tasks += [task]

            coins_founded_tasks = reduce(lambda a, b: a + b, await asyncio.gather(*tasks))
            get_coins_image_tasks = await asyncio.gather(*coins_founded_tasks)
        return get_coins_image_tasks

    def parse_coins(self):
        print(self.__category, self.__pattern)
        print(self.__url)
        coins = list(asyncio.run(self.__gather_data()))
        self.__coins.extend(coins)

    # tested
    @classmethod
    def __find_date(cls, txt):
        def get_date(date, pattern):
            try:
                return datetime.strptime(date, pattern)
            except ValueError:
                return None

        # Get current month
        month = datetime.today().strftime("%m")
        next_month = "{:02d}".format(int(month) % 12 + 1)
        date_pattern = [['\d{1,2}\.\d\d\.\d{4}', '%d.%m.%Y'],
                        ['\d{1,2}\.\d\d\.\d{2}', '%d.%m.%y'],
                        ['\d{1,2}\-\d\d\-\d{4}', '%d-%m-%Y'],
                        ['\d{1,2}\-\d\d\-\d{2}', '%d-%m-%y'],
                        ['\d{1,2}\/\d\d\/\d{4}', '%d/%m/%Y'],
                        ['\d{1,2}\/\d\d\/\d{2}', '%d/%m/%y'],
                        ['\d{1,2}/' + month, '%d/%m'],
                        ['\d{1,2}.' + month, '%d.%m'],
                        ['\d{1,2}-' + month, '%d-%m'],
                        ['\d{1,2}/' + next_month, '%d/%m'],
                        ['\d{1,2}.' + next_month, '%d.%m'],
                        ['\d{1,2}-' + next_month, '%d-%m'],
                        ]
        for date_pattern, pattern in date_pattern:
            dates = re.findall(date_pattern, txt)
            for date in dates:
                if get_date(date, pattern):
                    res = get_date(date, pattern)
                    if res.year == 1900:
                        res = res.replace(datetime.today().year)
                    return res

        return None

    @classmethod
    def __is_old_date(cls, date):
        # None date will be selected
        if date is None:
            return False
        now = datetime.today()
        return datetime(now.year, now.month, now.day) > date

    def __iter__(self):
        for item in self.__coins:
            yield item


def worktime(func):
    def wrapper(*args, **kwargs):
        st = time.time()
        func(*args, **kwargs)
        print(func.__name__, time.time() - st)

    return wrapper

#
@worktime
def main_async():
    param = [
        [116, '1921|1924|1925|1930|1931|1953|1983'],
        [118, '2002'],  # All unc
        [114, '1912'],  # cu
        [113, '1912'],  # ag/au
    ]
    coins = CoinsCollect()
    for category, pattern in param:
        coins.init(category, pattern)
        coins.parse_coins()
    print(coins.coins)


if __name__ == '__main__':
    main_async()

