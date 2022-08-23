# Navegar até https://f1races.netlify.app
# Extrair os dados:
# Nome de cada Grand Prix
# Local
# Nomde do piloto que venceu
# Tempo dele


import scrapy
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep


def iniciar_driver():
    chrome_options = Options()
    LOGGER.setLevel(logging.WARNING) # FAZ COM QUE SE EXIBA SOMENTE INFORMAÇÕES ACIMA DE WARNING NO CONSOLE
    arguments = ['--lang=pt-BR', '--window-size=1920,1080', '--headless'] # HEADLESS SEGUNDO PLANO
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait


class F1RacesScraperSpider(scrapy.Spider):
    # identidade
    name = 'racebot'
    # Request

    def start_requests(self):
        # não esqueça de setar ROBOTSTXT_OBEY = False dentro do arquivo settings.py
        urls = ['https://f1races.netlify.app']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proximo_url': url})
    # Response

    def parse(self, response):
        driver, wait = iniciar_driver()
        driver.get(response.meta['proximo_url'])
        sleep(10)
        response_webdriver = Selector(text=driver.page_source)

        for race in response_webdriver.xpath('//div[@class="sc-bZQynM llbHfj"]'):
            yield {
                'País': race.xpath('./div[1]/text()').get(),
                'Corrida': race.xpath('./div[2]/text()').get(),
                'Piloto': race.xpath('.//a/text()').get(),
                'Tempo': race.xpath('//div[@class="sc-htoDjs dubYDw"]/span/text()').get() + ' ' + race.xpath('./div[4]/text()').get() ,
            }
        driver.close()