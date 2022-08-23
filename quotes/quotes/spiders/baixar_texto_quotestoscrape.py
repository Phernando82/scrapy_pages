import scrapy

class QuotesToScrapeSpider(scrapy.Spider):
    # identidade
    name = 'texto_bot'
    # request
    def start_requests(self):
        # Definir as urls para varrer
        urls = ['https://quotes.toscrape.com/']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    # Response
    def parse(self, response):
        # Aqui é onde processamos o que é retornado da response
        # laço for para pegar mais de um elemento
        # usamos o xpath da div que contém todos os elementos que queremos buscar
        for elemento in response.xpath('//div[@class="quote"]'): 
            yield{
                'frase': elemento.xpath('.//span[@class="text"]/text()').get(), # xpath do texto 
                'autor': elemento.xpath('.//small[@class="author"]/text()').get(), # xpath do autor
                'tags': elemento.xpath('.//a[@class="tag"]/text()').getall() # xpath das tags
            } # Precisa colocar o . antes do xpath para ele buscar somente na div, senão busca
              # no site todo a cada iteração do laço (laço da página e não da div) e se o . traz 
              # traz x vezes o primeiro texto ao invés dos textos todos