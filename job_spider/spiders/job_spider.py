import scrapy
from job_spider.items import JobSpiderItem
from datetime import datetime, timedelta
import logging as log

"""
StackOverflow Jobs Spider
"""
class SO_Spider(scrapy.Spider):
    name = 'SO_Spider'

    # Some Filters
    offers_remote = True
    desired_techs = ['python']
    undesired_techs = ['ruby-on-rails']

    root_url = 'https://stackoverflow.com/jobs?'
    start_url = root_url
    if offers_remote:
        start_url = start_url + "r=true"
    if len(desired_techs) > 0:
        start_url += '&tl='
        for tech in desired_techs:
            start_url += tech
    if len(undesired_techs) > 0:
        start_url += '&td='
        for tech in undesired_techs:
            start_url += tech

    start_urls = [start_url + '&ms=MidLevel&mxs=Senior&j=permanent%2ccontract&ss=1&sort=p']

    def parse(self, response):
        for job in response.xpath('//div[@data-jobid]'):
            item = JobSpiderItem()
            item['provider'] = 'stackoverflow'
            item['id'] = job.xpath('.//@data-jobid').get()
            item['title'] = job.xpath('.//h2/a/text()').get()
            item['company'] = job.xpath('.//h3/span/text()').get().split('\r\n')[0]
            item['techs'] = job.xpath('.//div/div/a/text()').getall()
            item['url'] = self.root_url + job.xpath('.//a/@href').getall()[0]

            age_n_s = job.xpath('.//div/div/div/div[1]/text()').get()
            item['dt_posted'] = self.convert_friendly_date(age_n_s)
            item['dt_pulled'] = datetime.now()

            yield item

        for next_page in response.xpath("//div[@class='s-pagination']/a[span = 'next']"):
            yield response.follow(next_page, self.parse)

    # dates are given in "human friendly" format, so we need to reverse this awful niceness :O)
    # probably make this static if its possible to re-use it for other spiders
    def convert_friendly_date(self, fd):
        if '<' in fd:
            fd = fd[2:]

        age_n_s = fd.split()[0]
        age_n_l = []
        age_s_l = []
        for i in age_n_s:
            if i.isdigit():
                age_n_l.append(i)
            else:
                age_s_l.append(i)
        if age_n_s == 'yesterday':
            age_n = 1
            age_s = 'd'
        else:
            try:
                age_n = int(''.join(age_n_l))
                age_s = ''.join(age_s_l)
            except Exception as e:
                log.debug(f"fd: {fd}")
                log.debug(e)

        d = datetime.now()
        if age_s == 'd':
            d -= timedelta(days=age_n)
        elif age_s == 'h':
            d -= timedelta(hours=age_n)

        return d
