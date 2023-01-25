import asyncio
from datetime import datetime
from functools import reduce
import re

import aiohttp
from bs4 import BeautifulSoup


ROOT_URL = 'https://coins.lave.ru/forum'


class CoinsCollect:
    OLD_DATE = False

    _headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:79.0) '
                      'Gecko/20100101 Firefox/79.0',
    }

    def __init__(self, category, pattern, unc_pattern):
        self.__coins = []
        self.__category = category
        self.__pattern = pattern.lower()
        self.__unc_pattern = unc_pattern.lower() if unc_pattern else None
        self.__url = f'{ROOT_URL}/viewforum.php?f={category}'

    def __page_url(self, page):
        return f'{self.__url}&start={page}'

    def coin_url(self, coin_id):
        return f'{ROOT_URL}/viewtopic.php?f={self.__category}&t={coin_id}'

    @property
    def coins(self):
        return self.__coins

    @classmethod
    async def __get_img(cls, session, coin: dict):
        async with session.get(url=coin.get('url')) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')

            time_create = datetime.strptime(soup.find(
                'b', text='Добавлено:').find_parent(
                'td').text.strip(), 'Добавлено: %d-%m-%Y %H:%M:%S')
            if time_create:
                coin['time_create'] = time_create

            img_in = soup.find('img', src=re.compile(r'thumb\/'))
            img_out = soup.find('img', alt='Изображение')
            img_big = soup.find('img', src=re.compile(r'small\/'))
            img = img_in or img_out or img_big or None
            if img:
                coin['image'] = img.get('src', None)
        return coin

    async def _filter(self, date, title, desc) -> bool:
        def parse_filter() -> list:
            for item in self.__pattern.split('|'):
                yield item.split('&')

        searching = [
            (bool(re.search(filter_elem, title)) for filter_elem in filter_item)
            for filter_item in parse_filter()
        ]

        # Search unc in (title, desc)
        is_unc = bool(
            re.search(f'{self.__unc_pattern}', (title + desc).lower())
        ) if self.__unc_pattern else True

        is_not_old_date = not self.__is_old_date(date) or self.OLD_DATE

        return any(all([*item, is_unc, is_not_old_date]) for item in searching)

    async def __get_page_data(self, session, page_url):
        async with session.get(url=page_url) as response:
            tasks = []
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            tds = soup.find_all('a', class_='topictitle')
            for td in tds:
                title = td.text.strip()
                desc = td.get('title')
                date = self.__find_date(title + desc)
                if not await self._filter(date, title, desc):
                    continue

                url = td.get('href')[1:]
                absolute_url = f'{ROOT_URL}{url}'
                user = td.find_parent('tr').find(
                    'p', class_='topicauthor'
                ).text.strip()
                coin = dict(
                    category_id=self.__category,
                    url=absolute_url,
                    title=title,
                    image=None,
                    seller=user,
                    time_end=date,
                    time_create=None,
                )
                tasks += [asyncio.create_task(
                    self.__get_img(session, coin)
                )]
        return tasks

    async def __gather_data(self):
        async with aiohttp.ClientSession(headers=self._headers) as session:
            response = await session.get(url=self.__url)
            soup = BeautifulSoup(await response.text(), 'lxml')
            page_urls = soup.find(
                'td', class_="gensmall", align="right"
            ).find_all('a')
            pages_count = int(page_urls[-2].text) if page_urls else 1

            tasks = []
            for index in range(0, (pages_count - 1) * 50 + 1, 50):
                task = asyncio.create_task(
                    self.__get_page_data(
                        session,
                        self.__page_url(index)
                    )
                )
                tasks += [task]

            coins_founded_tasks = reduce(
                lambda a, b: a + b,
                await asyncio.gather(*tasks)
            )
            get_coins_image_tasks = await asyncio.gather(*coins_founded_tasks)
        return get_coins_image_tasks

    def parse_coins(self):
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
