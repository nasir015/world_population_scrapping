# -*- coding: utf-8 -*-

import re
from urllib import request
from urllib.parse import urljoin
import scrapy
import logging

class PopulationSpider(scrapy.Spider):
    name = 'population'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            # absolute_url = response.urljoin(link)
            
            
            yield response.follow(url=link, callback= self.parse_country, meta={'country_name':name})
    
    
    def parse_country(self, response):
        name= response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year =row.xpath(".//td[1]/text()").get()
            populations=row.xpath(".//td[2]/strong/text()").get()
            
            yield{
                'country_name':name,
                'year':year,
                'populations': populations
            }
            