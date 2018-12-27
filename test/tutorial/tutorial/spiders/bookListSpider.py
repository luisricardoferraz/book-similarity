import scrapy
import bookSpider

class BookListSpider(scrapy.Spider):
    name = 'book-list-spider'

    start_urls = [
        'https://www.skoob.com.br/editoras/'
    ]

    def parse(self,response):
        publishers = response.css('div#resultadoBusca- > div > div > a::attr("href")').extract()
        yield response.follow(publishers[11], self.findBooksList)
        

    def findBooksList(self, response):
        books = response.css('ul#ul-menu-vertical-badges > li > a.l13::attr("href")').extract()
        yield response.follow(books[2], self.findTitle)

    
    def findTitle(self,response):
        title = bookSpider.BookSpider()

        for book in response.css('div.box_livro'):
            link = 'https://www.skoob.com.br' + book.css('div > a.capa-link-item::attr("href")').extract_first()
            yield response.follow(link, title.extractData)
        
        nextPage = response.css('div.proximo a::attr("href")').extract_first()
        if nextPage is not None:
            yield response.follow(nextPage, self.findTitle)