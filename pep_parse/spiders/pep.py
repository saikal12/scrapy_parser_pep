import scrapy
from pep_parse.items import PepParseItem

from pep_parse.settings import ALLOWED_DOMAINS


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ALLOWED_DOMAINS
    start_urls = [f'https://{domains}/' for domains in allowed_domains]

    def parse(self, response):
        for peps_links in response.css(
                'a.pep.reference.internal::attr(href)'
        ).getall():
            yield response.follow(peps_links, callback=self.parse_pep)

    def parse_pep(self, response):
        string = response.css('h1.page-title::text').get().split(' ')
        data = {
            'number': int(string[1]),
            'name': ' '.join(string[3:]),
            'status': response.css('dt:contains("Status") + dd ::text').get()
        }
        yield PepParseItem(data)
