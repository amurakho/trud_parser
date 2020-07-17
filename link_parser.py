import requests
from bs4 import BeautifulSoup
import typing
import logging

# https://trud.ua/jobs/list/q/{keyword}/filter_show/state/page/{page_number}
class Not200StatusCode(Exception):
    pass


class LinkParser:
    base_url = 'https://trud.ua/jobs/list/q/{keyword}/filter_show/state'
    pagination = '/page/{page_number}'

    def __init__(self,  is_paginate=True):
        self.is_paginate = is_paginate
        self.data = []

    def _pagination(self, page_number):
        pass

    def _parse_blocks(self, block: str) -> list:
        pass

    def parse_content(self, content: bytes, page_number=2) -> typing.List[dict]:
        soup = BeautifulSoup(content, 'lxml')

        blocks = soup.find_all(class_="result-unit")

        data = self._parse_blocks(blocks)
        self.data.extend(data)

        last_page = soup.find(class_='yiiPager').find(class_='next-p disabled')
        if self.is_paginate and not last_page:
            content = self._pagination(page_number)
            self.parse_content(content, page_number+1)


    def pass_request(self, keyword) -> bytes:
        self.base_url = self.base_url.format(keyword=keyword)
        print('INFO: Url is: ', self.base_url)

        response = requests.get(self.base_url)

        if not response.status_code == 200:
            raise Not200StatusCode('Status code is: ', response.status_code)

        print('INFO: Status code is 200')

        return response.content

    def start(self, keyword):

        content = self.pass_request(keyword)

        data = self.parse_content(content)