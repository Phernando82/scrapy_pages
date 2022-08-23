import scrapy
from scrapy.loader import ItemLoader
from quotes.items import QuotesItem

# Colocar o nome dos autores em maisculas
# Mudar separador das tags de , para ;

# Como varrer várias páginas

class QuotesToScrapeSpider(scrapy.Spider):
    # identidade
    name = 'good_reads_bot'
    # request
    def start_requests(self):
        # Definir as urls para varrer
        urls = ['https://www.goodreads.com/quotes']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    # Response
    def parse(self, response):
        # Aqui é onde processamos o que é retornado da response
        for elemento in response.xpath("//div[@class='quote']"): 
            loader = ItemLoader(item=QuotesItem(),selector=elemento, response=response)
            loader.add_xpath('frase',".//div[@class='quoteText']/text()")
            loader.add_xpath('autor', ".//span[@class='authorOrTitle']/text()")
            loader.add_xpath('tags', ".//div[@class='greyText smallText left']//a/text()")
            yield loader.load_item()
        try:
            link_href = response.xpath('//a[@class="next_page"]/@href').get()
            if link_href is not None:
                link_next = response.urljoin(link_href)
                yield scrapy.Request(url=link_next, callback=self.parse)
        except:
            # se não encontrar, o programa deve parar
            print('Última página')
   
    