import scrapy

# Como varrer várias páginas

class QuotesToScrapeSpider(scrapy.Spider):
    # identidade
    name = 'good_reads_2_bot'
    # request
    def start_requests(self):
        # Definir as urls para varrer
        urls = ['https://www.goodreads.com/quotes?page=1']

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
            } # Precisa colocar o . antes do xpath para ele buscar somente na div, senão busca
              # no site todo a cada iteração do laço (laço da página e não da div) e se o . traz 
              # traz x vezes o primeiro texto ao invés dos textos todos

    # Encontrar o link para a próxima página e extrair o número da próxima página
        try:
            numero_pagina = response.xpath('//a[@class="next_page"]/@href').get().split('=')[1]
            print('#'*20)
            print(numero_pagina)
            print('#'*20)
            if numero_pagina is not None:
                link_next = f'https://www.goodreads.com/quotes?page={numero_pagina}'
                print('#'*20)
                print(link_next)
                yield scrapy.Request(url=link_next, callback=self.parse)
        except:
            # se não encontrar, o programa deve parar
            print('Última página')
   
    