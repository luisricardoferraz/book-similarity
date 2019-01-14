# Import framework to create the crawler
import scrapy
import re
#import pandas

# Define crawler as a class derived from class Spider
class BookSpider(scrapy.Spider):

    # Define crawler's name
    #def __init__(self):
    #    self.name = 'book-spider'
    name = 'bookspider'

    start_urls = [
        'https://www.skoob.com.br/livro/580710ED582043', #Vários autores
        'https://www.skoob.com.br/obsidiana-520494ed527702.html', #Somente ISBN-13
        'https://www.skoob.com.br/john-lennon-em-nova-york-514655ed521321.html', #Autor no meio do Subtítulo
        'https://www.skoob.com.br/minha-sentenca-e-voce-839944ed845035.html', #Poucas estatísticas
        'https://www.skoob.com.br/a-sociedade-do-anel-13988ed3654.html', #Livro com várias tags
        'https://www.skoob.com.br/o-sal-da-vida-349935ed839186.html' #Livro sem sinopse
    ]


    # Define the callback function parse(), executed after receiving a response of the request
    #def extractData(self, response):
    def parse(self, response):    
        # Separate data into different groups and then store them into variables
        isbn = self.fixIsbnIfNull(response.css('div.sidebar-desc > span::text').extract())
        titulo = response.css('.sidebar-titulo::text').extract_first()
        subtitulo = response.css('.sidebar-subtitulo::text').extract()
        autor = self.checkAuthorExistence(response.css('div#pg-livro-menu-principal-container > a::text').extract(), response.css('div#pg-livro-menu-principal-container > i.sidebar-subtitulo::text').extract())
        editora = response.css('div.sidebar-desc > a::text').extract_first()
        detalhes = self.splitDetails(response.css('div.sidebar-desc').extract_first().split('<br>'))
        estatisticas = self.organizeStats(response.css('div#livro-perfil-status b > a::text').extract())
        nota = response.css('div#pg-livro-box-rating span.rating::text').extract_first()
        maisEstatisticas = self.organizeMoreStats(response.css('a.l_icones::text').extract())
        distribuicaoNotas = self.organizeRatingsDistribution(response.css('div.pg-livro-box-avaliacoes-grafico > div > div > div::text').extract())
        avaliacoesHomens = response.css('span.pg-livro-icone-male-label::text').extract_first()
        avaliacoesMulheres = response.css('span.pg-livro-icone-female-label::text').extract_first()
        generos = self.checkGendersExistence(response.css('span.pg-livro-generos::text').extract_first())
        tags = response.css('ul#tags > li.litags > a::text').extract()    
        sinopse = response.css('div#livro-perfil-sinopse-txt > p::text').extract()

        # Assembly new meanings for the data collected so it can be written in a .json file
        yield {
            'isbn-10': isbn.get("isbnTenDigits"),
            'isbn-13': isbn.get("isbnThirteenDigits"),
            'titulo': titulo,
            'subtitulo': subtitulo,
            'autor': autor,
            'editora': editora,
            'ano': detalhes.get("year"),
            'paginas': detalhes.get("pages"),
            'idioma': detalhes.get("idiom"),
            'leram': estatisticas.get("read"),
            'lendo': estatisticas.get("reading"),
            'queremLer': estatisticas.get("wantToRead"),
            'relendo': estatisticas.get("reReading"),
            'abandonos': estatisticas.get("abandoned"),
            'resenhas': estatisticas.get("reviews"),
            'nota': nota,
            'favoritos': maisEstatisticas.get("favorites"),
            'desejados': maisEstatisticas.get("wanted"),
            'trocam': maisEstatisticas.get("exchange"),
            'avaliaram': maisEstatisticas.get("rated"),
            'cincoEstrelas': distribuicaoNotas.get("fiveStars"),
            'quatroEstrelas': distribuicaoNotas.get("fourStars"),
            'tresEstrelas': distribuicaoNotas.get("threeStars"),
            'duasEstrelas': distribuicaoNotas.get("twoStars"),
            'umaEstrela': distribuicaoNotas.get("oneStar"),
            'avaliacoesHomens': avaliacoesHomens,
            'avaliacoesMulheres': avaliacoesMulheres,
            'generos': generos,
            'tags': tags,
            'sinopse': sinopse
        }

    def fixIsbnIfNull(self, isbnList):
        isbnDictionary = {
            "isbnThirteenDigits" : "",
            "isbnTenDigits" : ""
        }
        for isbn in isbnList:
            if len(isbn) == 13:
                isbnDictionary["isbnThirteenDigits"] = isbn
            elif len(isbn) == 10:
                isbnDictionary["isbnTenDigits"] = isbn
        return isbnDictionary
    
    def checkAuthorExistence(self, registeredAuthor, notRegisteredAuthor):
        if len(registeredAuthor) != 0:
            return registeredAuthor
        elif len(notRegisteredAuthor) != 0:
            return notRegisteredAuthor

    def splitDetails(self, detailsBlock):
        detailsDictionary = {
            "idiom" : "",
            "year" : "",
            "pages" : ""
        }
        detailsDictionary["idiom"] = detailsBlock[-3]
        detailsDictionary["year"] = detailsBlock[-4].split('/')[0]
        detailsDictionary["pages"] = detailsBlock[-4].split('/')[1]
        return detailsDictionary
    
    def organizeStats(self, bookStats):
        statsDictionary = {
            "read" : "",
            "reading" : "",
            "wantToRead" : "",
            "reReading" : "",
            "abandoned" : "",
            "reviews" : ""
        }
        statsDictionary["read"] = bookStats[-1]
        statsDictionary["reading"] = bookStats[-2]
        statsDictionary["wantToRead"] = bookStats[-3]
        statsDictionary["reReading"] = bookStats[-4]
        statsDictionary["abandoned"] = bookStats[-5]
        statsDictionary["reviews"] = bookStats[-6]
        return statsDictionary
    
    def organizeMoreStats(self, otherBookStats):
        moreStatsDictionary = {
            "favorites" : "",
            "wanted" : "",
            "exchange" : "",
            "rated" : ""
        }

        moreStatsDictionary["favorites"] = otherBookStats[0]
        moreStatsDictionary["wanted"] = otherBookStats[1]
        moreStatsDictionary["exchange"] = otherBookStats[2]
        moreStatsDictionary["rated"] = otherBookStats[3]
        return moreStatsDictionary
    
    def organizeRatingsDistribution(self, ratingsList):
        ratingsDistributionDictionary = {
            "fiveStars": "",
            "fourStars" : "",
            "threeStars" : "",
            "twoStars" : "",
            "oneStar" : ""
        }
        ratingsDistributionDictionary["fiveStars"] = ratingsList[0]
        ratingsDistributionDictionary["fourStars"] = ratingsList[1]
        ratingsDistributionDictionary["threeStars"] = ratingsList[2]
        ratingsDistributionDictionary["twoStars"] = ratingsList[3]
        ratingsDistributionDictionary["oneStar"] = ratingsList[4]
        return ratingsDistributionDictionary
    
    def checkGendersExistence(self, gendersList):
        if gendersList is not None and len(gendersList) != 0:
            return gendersList.split(' / ')
        else:
            return []
