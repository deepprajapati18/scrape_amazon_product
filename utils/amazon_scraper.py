import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AmazonScrapper:
    def __init__(self, keyword: str):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
        self.base_url = 'https://www.amazon.in'

        # generate URL
        formatted_keyword = '+'.join(keyword.split(' '))
        self.url = f'{self.base_url}/s?k={formatted_keyword}'
        logger.info(self.url)
        self.cards = []
        self.result = []

    def _trigger_url_and_get_page_content(self):
        # HTTP Request
        self.webpage = requests.get(self.url, headers=self.headers)
        # Soup Object containing all data
        if self.webpage.status_code != 200:
            return False, self.webpage.json()
        self.soup = BeautifulSoup(self.webpage.content, 'lxml')
        logger.info('Url triggerd and content fetched')

    def _collect_product_cards(self):
        """Collect all the product cards from Page"""
        self.cards = self.soup.find_all(
            'div', attrs={'data-component-type': 's-search-result'}
        )
        logger.info('Product Cards collected')

    def __get_image_from_card(self, card: BeautifulSoup) -> str:
        """Get Image from the Product Card"""
        image = card.find('img', attrs={'class': 's-image'})
        return image['src']

    def __get_title_from_card(self, card: BeautifulSoup) -> str:
        """Get Product Title from Product Card"""
        title = card.find('h2')
        return title.get_text()

    def __get_price_from_card(self, card: BeautifulSoup) -> str:
        """Get Product Price from Product Card"""
        price = card.find('span', attrs={'class': 'a-price'})
        return price.find('span').text if price else ''

    def __get_link_from_card(self, card: BeautifulSoup) -> str:
        """Get Product Link from Product Card"""
        link = card.find('a').get('href')
        return f'{self.base_url}{link}' if link else ''

    def __get_ratings_and_count_from_card(self, card: BeautifulSoup) -> list:
        """Get Product rating and count from Product Card"""
        rate = card.find('div', attrs={'class': 'a-row a-size-small'})
        if rate:
            return [i.get('aria-label') for i in rate]
        return ['', '']

    def _collect_data_from_cards(self):
        """Collect Required Product details from the Product Card"""
        logger.info('Product Details collection: Started')
        for card in self.cards:
            image = self.__get_image_from_card(card)
            title = self.__get_title_from_card(card)
            price = self.__get_price_from_card(card)
            link = self.__get_link_from_card(card)
            rate = self.__get_ratings_and_count_from_card(card)
            self.result.append(
                {
                    'link': link,
                    'image': image,
                    'title': title,
                    'price': price,
                    'ratings': rate[0],
                    'rating_count': rate[1],
                }
            )
        logger.info('Product Details collection: End')

    def do_process(self) -> tuple:
        """Process the Amazon Scrapper"""
        logger.info('Scrapper started')
        self._trigger_url_and_get_page_content()
        self._collect_product_cards()
        self._collect_data_from_cards()
        logger.info('Scrapper Ended')
        return True, self.result
