import scrapy
from scrapy.http import HtmlResponse
from jobparser.jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//div[@class ='_3mfro PlM3e _2JVkc _3LJqf']/a/@href").extract()
        for link in links:
            yield response.follow(link, callback = self.vacancy_parse)
        next_page = response.css("a.f-test-button-dalshe:attr('href')").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response:HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").extract_first()
        vacancy_salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        vacancy_link = response.url
        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, link=vacancy_link)