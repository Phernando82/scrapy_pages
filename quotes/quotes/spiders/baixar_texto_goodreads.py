# Crie um spider que navega até o site https://www.goodreads.com/quotes
# Extrai todas as citações, autores e tags que estão na página
# Exporte esse resultado para um arquivo CSV

import scrapy

class QuotesToScrapeSpider(scrapy.Spider):
    # identidade
    name = 'quotes_bot'
    # request
    def start_requests(self):
        # Definir as urls para varrer
        urls = ['https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    # Response
    def parse(self, response):
        # Aqui é onde processamos o que é retornado da response
        # laço for para pegar mais de um elemento
        # usamos o xpath da div que contém todos os elementos que queremos buscar
        for elemento in response.xpath('//div[@class="quote"]'): 
            yield{
                'frase': elemento.xpath('.//div[@class="quoteText"]/text()').get(), # xpath do texto 
                'autor': elemento.xpath('.//span[@class="authorOrTitle"]/text()').get(), # xpath do autor
                'tags': elemento.xpath('.//div[@class="greyText smallText left"]//a/text()').getall(), # xpath das tags
                'links': elemento.xpath(response.urljoin('.//div[@class="greyText smallText left"]//a/@href')).getall() # xpath dos links
            } # Precisa colocar o . antes do xpath para ele buscar somente na div, senão busca
              # no site todo a cada iteração do laço (laço da página e não da div) e se o . traz 
              # traz x vezes o primeiro texto ao invés dos textos todos response.urljoin('.//div[@class="greyText smallText left"]//a/@href')