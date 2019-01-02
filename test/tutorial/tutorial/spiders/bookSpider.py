# Import framework to create the crawler
import scrapy

# Define crawler as a class derived from class Spider
class BookSpider(scrapy.Spider):

    # Define crawler's name
    def __init__(self):  
        name = 'book-spider'

    # Define the callback function parse(), executed after receiving a response of the request
    def extractData(self, response):
        
        # Separate data into different groups and then store them into variables
        stats = response.css('div#livro-perfil-status b > a::text').extract()
        rating = response.css('div#pg-livro-box-rating span.rating::text').extract_first()
        totalAvaliacoes = response.css('div#pg-livro-box-rating-avaliadores-numero::text').extract_first()
        maisStats = response.css('a.l_icones::text').extract()
        titulo = response.css('.sidebar-titulo::text').extract_first()
        autor = response.css('div#pg-livro-menu-principal-container > a::text').extract_first()
        detalhes = response.css('div.sidebar-desc').extract_first()
        sinopse = response.css('div#livro-perfil-sinopse-txt > p').extract_first()
        generos = response.css('span.pg-livro-generos::text').extract_first()
        notas = response.css('div.pg-livro-box-avaliacoes-grafico > div > div > div::text').extract()
        tags = response.css('ul#tags > li.litags > a::text').extract()
        avaliacoesHomens = response.css('span.pg-livro-icone-male-label::text').extract_first()
        avaliacoesMulheres = response.css('span.pg-livro-icone-female-label::text').extract_first()
        subtitulo = response.css('.sidebar-subtitulo::text').extract()

        # Assembly new meanings for the data collected so it can be written in a .json file
        yield {
            'titulo': titulo,
            'subtitulo': subtitulo,
            'autor': autor,
            'detalhes': detalhes,
            'leram': stats[-1],
            'lendo': stats[-2],
            'queremLer': stats[-3],
            'relendo': stats[-4],
            'abandonos': stats[-5],
            'resenhas': stats[-6],
            'rating': rating,
            'totalAvaliacoes': totalAvaliacoes,
            'favoritos': maisStats[0],
            'desejados': maisStats[1],
            'trocam': maisStats[2],
            'avaliaram': maisStats[3],
            'generos': generos,
            'cincoEstrelas': notas[0],
            'quatroEstrelas': notas[1],
            'tresEstrelas': notas[2],
            'duasEstrelas': notas[3],
            'umaEstrela': notas[4],
            'tags': tags,
            'avaliacoesHomens': avaliacoesHomens,
            'avaliacoesMulheres': avaliacoesMulheres,
            'sinopse': sinopse
        }