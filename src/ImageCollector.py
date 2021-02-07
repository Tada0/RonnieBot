from random import choice
import requests
from bs4 import BeautifulSoup
import re
import json


class ImageCollector:
    YAHOO_IMAGES_URL = 'https://images.search.yahoo.com'

    @staticmethod
    def get_random_ronnie_image_url():
        result = requests.get(f'{ImageCollector.YAHOO_IMAGES_URL}/search/images;?p=ronnie+coleman')
        yahoo_soup = BeautifulSoup(result.text, 'html.parser')
        chosen_image_tag = choice(yahoo_soup.findAll('a', {'aria-label': re.compile(r'.+')}))
        image_url_data = requests.get(f'{ImageCollector.YAHOO_IMAGES_URL}{chosen_image_tag["href"]}')
        image_soup = BeautifulSoup(image_url_data.text, 'html.parser')
        image_data = json.loads(image_soup.findAll('script', {'type': "text/javascript"})[-1].string[8:])
        return choice(image_data["results"])["iurl"]
