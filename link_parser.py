import requests
from bs4 import BeautifulSoup
import typing
import logging

# https://trud.ua/jobs/list/q/{keyword}/filter_show/state/page/{page_number}
class Not200StatusCode(Exception):
    pass


class LinkParser:
    url = 'https://trud.ua/jobs/'
    base_url = 'https://trud.ua/jobs/list/q/{keyword}/filter_show/state'
    pagination = '/page/{page_number}'

    def __init__(self,  is_paginate=True):
        self.is_paginate = is_paginate
        self.data = []
        self.keyword = ''

    def _pagination(self, page_number):
        url = self.base_url.format(keyword=self.keyword) + self.pagination.format(page_number=page_number)
        response = requests.get(url)
        requests.Session()
        return response.content

    def _get_value(self, table_block,  selector):
        row = table_block.find('div', {'class': selector})
        if row:
            return row.get_text()

    def _parse_blocks(self, blocks: str) -> list:
        data = []
        for block in blocks:
            title_block = block.find('div', {
                'class': 'titl-r'
            })
            table_block = block.find('div', {'class': 'table-view'})
            d = {
                'title': title_block.get_text(),
                'uploaded_date': self._get_value(table_block, 'date'),
                'company_url': table_block.find('div', {'class': 'institution'}).find('a').get('href'),
                'company_name': self._get_value(table_block, 'institution'),
                'location': self._get_value(table_block, 'location'),
                'salary': self._get_value(table_block, 'salary'),
                'text': self._get_value(table_block, 'descr-r'),
                'url': title_block.find('a').get('href'),
            }
            data.append(d)
        return data

    def parse_content(self, content: bytes, page_number=2) -> typing.List[dict]:
        soup = BeautifulSoup(content, 'lxml')

        blocks = soup.find_all(class_="result-unit")

        data = self._parse_blocks(blocks)
        self.data.extend(data)
        print('INFO: already parsed {} rows'.format(len(self.data)))

        last_page = soup.find(class_='yiiPager').find(class_='next-p disabled')
        if self.is_paginate and not last_page:
            print('INFO: Try to paginate. Page numbe', page_number)
            content = self._pagination(page_number)

            self.parse_content(content, page_number+1)
        return self.data

    def pass_request(self) -> bytes:
        self.base_url = self.base_url.format(keyword=self.keyword)
        print('INFO: Url is: ', self.base_url)

        response = requests.get(self.base_url)

        if not response.status_code == 200:
            raise Not200StatusCode('Status code is: ', response.status_code)

        print('INFO: Status code is 200')

        return response.content

    def start(self, keyword):
        self.keyword = keyword

        content = self.pass_request()

        data = self.parse_content(content)

        # print(len(data))