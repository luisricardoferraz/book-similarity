# Import Frameworks to create the crawler
import scrapy
from tutorial.spiders import bookSpider

# Define crawler as a class derived from class Spider
class BookListSpider(scrapy.Spider):

    # Define crawler's name
    name = 'book-list-spider'

    # Start crawler with the list of publishers in Skoob
    start_urls = [
        'https://www.skoob.com.br/editoras/'
    ]

    # Define the function parse(), executed once request succeeds
    def parse(self, response):

        # Extract links for publishers
        publishers = response.css('div#resultadoBusca- > div > div > a::attr("href")').extract()

        # Execute method findBooksList() after following each link
        for publisher in publishers:
            yield response.follow(publisher, self.findBooksList)
        
    # Find links for books published by a publisher
    def findBooksList(self, response):
        books = response.css('ul#ul-menu-vertical-badges > li > a.l13::attr("href")').extract()
        # Execute method findTitle() after following each link
        yield response.follow(books[2], self.findTitle)

    
    # Extract book data
    def findTitle(self, response):

        # Create a BookSpider object
        title = bookSpider.BookSpider()

        # For each book published by a publisher
        for book in response.css('div.box_livro'):
            
            # Find its link
            link = 'https://www.skoob.com.br' + book.css('div > a.capa-link-item::attr("href")').extract_first()

            # Follow the link and extract data using the BookSpider object
            yield response.follow(link, title.extractData)
        
        # Check whether there's more than one page of books published; if so, follow them
        nextPage = response.css('div.proximo a::attr("href")').extract_first()

        if nextPage is not None:
            # If there's a next page, extract book data recursively
            yield response.follow(nextPage, self.findTitle)