# Import framework to create the crawler
import scrapy

# Define crawler as a class derived from class Spider
class BookSpider(scrapy.Spider):

    # Define crawler's name
    def __init__(self):
        self.name = 'book-spider'

    # Define the callback function extractData(), executed once the request succeeds
    def extractData(self, response):

        # Separate data into different groups and then store them into variables
        # There is no standard in Skoob pages and they may lack some data, so additional methods were required
        isbn = self.checkIsbnExistence(response.css('div.sidebar-desc > span::text').extract())
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
        sinopse = self.printWholeSynopsis(response.css('div#livro-perfil-sinopse-txt > p::text').extract())

        # Assembly new meanings for the data collected so it can be written in an output file
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
    
    # Check whether a book has a 10-digit or 13-digit ISBN, or none of them 
    def checkIsbnExistence(self, isbnList):
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
    
    # Get the author regardless whether they are registered or not
    def checkAuthorExistence(self, registeredAuthor, notRegisteredAuthor):
        if len(registeredAuthor) != 0:
            return registeredAuthor
        elif len(notRegisteredAuthor) != 0:
            return notRegisteredAuthor

    # Explode a string which contains lots of data
    def splitDetails(self, detailsBlock):
        detailsDictionary = {
            "idiom" : "",
            "year" : "",
            "pages" : ""
        }
        detailsDictionary["idiom"] = detailsBlock[-3]
        detailsDictionary["year"] = self.removeDots(detailsBlock[-4].split('/')[0])
        detailsDictionary["pages"] = self.removeDots(detailsBlock[-4].split('/')[1])
        return detailsDictionary

    # Store book main stats properly    
    def organizeStats(self, bookStats):
        statsDictionary = {
            "read" : "",
            "reading" : "",
            "wantToRead" : "",
            "reReading" : "",
            "abandoned" : "",
            "reviews" : ""
        }
        statsDictionary["read"] = self.removeDots(bookStats[-1])
        statsDictionary["reading"] = self.removeDots(bookStats[-2])
        statsDictionary["wantToRead"] = self.removeDots(bookStats[-3])
        statsDictionary["reReading"] = self.removeDots(bookStats[-4])
        statsDictionary["abandoned"] = self.removeDots(bookStats[-5])
        statsDictionary["reviews"] = self.removeDots(bookStats[-6])
        return statsDictionary
    
    # Store other book stats properly
    def organizeMoreStats(self, otherBookStats):
        moreStatsDictionary = {
            "favorites" : "",
            "wanted" : "",
            "exchange" : "",
            "rated" : ""
        }

        moreStatsDictionary["favorites"] = self.removeDots(otherBookStats[0])
        moreStatsDictionary["wanted"] = self.removeDots(otherBookStats[1])
        moreStatsDictionary["exchange"] = self.removeDots(otherBookStats[2])
        moreStatsDictionary["rated"] = self.removeDots(otherBookStats[3])
        return moreStatsDictionary
    
    # Store ratings distribution properly
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
    
    # Check whether a book has a gender or not
    def checkGendersExistence(self, gendersList):
        if gendersList is not None and len(gendersList) != 0:
            return gendersList.split(' / ')
        else:
            return []
    
    # Remove dots if number is greater than a thousand
    def removeDots(self, number):
        if '.' in number:
            return number.replace('.','')
        else:
            return number
    
    # Concatenate all elements of synopsis into one string
    def printWholeSynopsis(self, synopsis):
        cleanSynopsis = ''

        for quote in synopsis:
            cleanSynopsis += quote + ' '

        return cleanSynopsis
