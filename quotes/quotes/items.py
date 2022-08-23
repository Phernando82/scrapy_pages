# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html



import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def tirar_espaco_em_branco(valor):
    return valor.strip()

def processar_caracteres_especiais(valor):
    return valor.replace(u"\u201c",'').replace(u"\u201d",'').replace(u"\u2014",'—')

def colocar_em_maiusculo(valor):
    return valor.upper()


class QuotesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    frase = scrapy.Field(
        input_processor=MapCompose(tirar_espaco_em_branco,processar_caracteres_especiais),
        output_processor=TakeFirst()
    )
    autor = scrapy.Field(
        input_processor=MapCompose(colocar_em_maiusculo, tirar_espaco_em_branco),
        output_processor=TakeFirst() # vai fazer o .get() direto sem tratar
    )
        
    tags = scrapy.Field(
        output_processor=Join(';') # vai pegar as tags que estão separadas e unir em uma separada por ;
    )
    

   
   

# MapCompose chama funções que tratam a string - tirar espaço em branco por ex.
# Takefirst é o mesmo que get()