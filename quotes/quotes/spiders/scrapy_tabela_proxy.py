import scrapy

class VarrerTabela(scrapy.Spider):
    # identidade
    name = 'varrer_tabela_spider'
    # Request
    def start_requests(self):
        urls = ['https://www.us-proxy.org/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        # Montar um XPATH que retorna a linha
        for linha in response.xpath('//table[@class="table table-striped table-bordered"]//tr'):
            yield{
                # Montar xpath para cada item 
                'IP Address': linha.xpath('./td[1]/text()').get(),
                'Port': linha.xpath('./td[2]/text()').get(),
                'Code': linha.xpath('./td[3]/text()').get(),
                'Country': linha.xpath('./td[4]/text()').get(),
                'Anonymity': linha.xpath('./td[5]/text()').get(),
                'Google': linha.xpath('./td[6]/text()').get(),
                'Https': linha.xpath('./td[7]/text()').get(),
                'Last Checked': linha.xpath('./td[8]/text()').get()
            }

