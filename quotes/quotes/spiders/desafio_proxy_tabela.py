# site: https://free-proxy-list.net/web-proxy.html

import scrapy

class VarrerTabela(scrapy.Spider):
    # identidade
    name = 'desafio_tabela_spider'
    # Request
    def start_requests(self):
        urls = ['https://free-proxy-list.net/web-proxy.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        # Montar um XPATH que retorna a linha
        for linha in response.xpath('//table[@class="table table-striped table-bordered"]//tr'):
            yield{
                # Montar xpath para cada item 
                'Proxy Name': linha.xpath('./td[1]/a/text()').get(),
                'Domain': linha.xpath('./td[2]/text()').get(),
                'Country': linha.xpath('./td[3]/text()').get(),
                'Speed': linha.xpath('./td[4]/text()').get(),
                'Popularity': linha.xpath('./td[5]//div/text()').get(),
            }

