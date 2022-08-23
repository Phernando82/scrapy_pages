import scrapy

class QuotesToScrapeSpider(scrapy.Spider):
    # identidade
    name = 'html_bot'
    # request
    def start_requests(self):
        # Definir as urls para varrer
        urls = ['https://quotes.toscrape.com/']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    # Response
    def parse(self, response):
        # Aqui é onde processamos o que é retornado da response
        with open('quotes.html', 'wb') as arquivo:
            arquivo.write(response.body)