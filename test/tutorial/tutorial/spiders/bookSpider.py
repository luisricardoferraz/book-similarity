# Import framework to create the crawler
import scrapy
import re

# Define crawler as a class derived from class Spider
class BookSpider(scrapy.Spider):

    # Define crawler's name
    def __init__(self):  
        self.name = 'book-spider'


    # Define the callback function parse(), executed after receiving a response of the request
    def extractData(self, response):
        
        # Separate data into different groups and then store them into variables
        stats = response.css('div#livro-perfil-status b > a::text').extract()
        rating = response.css('div#pg-livro-box-rating span.rating::text').extract_first()
        maisStats = response.css('a.l_icones::text').extract()
        titulo = response.css('.sidebar-titulo::text').extract_first()
        autor = response.css('div#pg-livro-menu-principal-container > a::text').extract_first()
        detalhes = self.cleanDetailsArray(response.css('div.sidebar-desc').extract_first().split('<br>'))
        isbn = self.fixIsbnIfNull(response.css('div.sidebar-desc > span::text').extract())
        sinopse = self.printWholeSynopsis(response.css('div#livro-perfil-sinopse-txt > p::text').extract())
        generos = response.css('span.pg-livro-generos::text').extract_first().split(' / ')
        notas = response.css('div.pg-livro-box-avaliacoes-grafico > div > div > div::text').extract()
        tags = response.css('ul#tags > li.litags > a::text').extract()
        avaliacoesHomens = response.css('span.pg-livro-icone-male-label::text').extract_first()
        avaliacoesMulheres = response.css('span.pg-livro-icone-female-label::text').extract_first()
        subtitulo = response.css('.sidebar-subtitulo::text').extract()

        # Assembly new meanings for the data collected so it can be written in a .json file
        yield {
            'isbn-10': isbn[1].strip(),
            'isbn-13': isbn[0].strip(),
            'titulo': titulo.strip(),
            'subtitulo': subtitulo,
            'autor': autor.strip(),
            'editora': detalhes[0].strip(),
            'ano': re.search('([0-9]+)', self.removeDots(detalhes[2])).group(),
            'paginas': re.search('([0-9]+)', self.removeDots(detalhes[3])).group(),
            'idioma': re.search('([^ ]+)', self.removeDots(detalhes[1])).group(),
            'leram': self.removeDots(stats[-1]),
            'lendo': self.removeDots(stats[-2]),
            'queremLer': self.removeDots(stats[-3]),
            'relendo': self.removeDots(stats[-4]),
            'abandonos': self.removeDots(stats[-5]),
            'resenhas': self.removeDots(stats[-6]),
            'rating': rating.strip(),
            'favoritos': re.search('([0-9]+)', self.removeDots(maisStats[0])).group(),
            'desejados': re.search('([0-9]+)', self.removeDots(maisStats[1])).group(),
            'trocam': re.search('([0-9]+)', self.removeDots(maisStats[2])).group(),
            'avaliaram': re.search('([0-9]+)', self.removeDots(maisStats[3])).group(),
            'generos': generos,
            'cincoEstrelas': notas[0].strip(),
            'quatroEstrelas': notas[1].strip(),
            'tresEstrelas': notas[2].strip(),
            'duasEstrelas': notas[3].strip(),
            'umaEstrela': notas[4].strip(),
            'tags': tags,
            'avaliacoesHomens': avaliacoesHomens.strip(),
            'avaliacoesMulheres': avaliacoesMulheres.strip(),
            'sinopse': sinopse.strip()
        }
    
    def printWholeSynopsis(self, synopsis):
        wholeText = ''

        for text in synopsis:
            wholeText += text
        
        return wholeText
    
    def fixIsbnIfNull(self, isbn):
        return isbn + ['','']

    def cleanDetailsArray(self, detalhes):
        details = ['','','','']
        details[0] = detalhes[-2].split(':')[1]
        details[1] = detalhes[-3].split(':')[1]
        details[2] = detalhes[-4].split('/')[0].split(':')[1]
        details[3] = detalhes[-4].split('/')[1].split(':')[1]
        return details
    
    def removeDots(self, string):
        return string.replace('.','')