import scrapy
import re
import json

class IndeedcrawlerSpider(scrapy.Spider):
    name = "indeedcrawler"
    allowed_domains = ["indeed.com"]
    # start_urls = ["https://indeed.com"]

    headers = {
        "Cookie": 'app="186.0,Android"; appSignIn=1; CTK=1ibu340lki0gk801; Device-ID=1ibu340mvi0gk801',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Phone Build/RQ1A.210105.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Mobile Safari/537.36 Indeed App 186.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.indeed.android.jobsearch",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }


    def __init__(self, company_name = 'Government Tactical Solutions LLC'):
        self.company_name=company_name

    def start_requests(self):
        yield scrapy.Request(r'https://www.indeed.com/m/jobs?q='+self.company_name+r'&l=&from=searchOnHP&sameL=1',headers=self.headers,callback=self.parse_fcckey)

    def parse_fcckey(self, response):
        pattern = r'window\._initialData\s*=\s*(\{.*\});'
        fcckey=''
        
        match = re.search(pattern, response.text, re.DOTALL)
        
        if match:
            initial_data = match.group(1)
            
            d=json.loads(initial_data.split('\n')[0].replace('};','}'))
            for filter in d['dynFiltersViewModel']['filters']:
                if filter['filterName']=='fcckey':
                    for option in filter['options']:
                        if option['label']==self.company_name:
                            fcckey=option['paramValMap']['fcckey']
                            break
                    break
        if fcckey=='':
            yield scrapy.Request(r'https://www.indeed.com/m/jobs?q='+self.company_name+r'&l=&from=searchOnHP&sameL=1',headers=self.headers,callback=self.parse_fcckey,dont_filter=True)
        else:
            yield scrapy.Request(r'https://www.indeed.com/m/jobs?q='+self.company_name+r'&l=&sc=0kf%3Afcckey%28'+fcckey,headers=self.headers,callback=self.parse_joblinks)

    def parse_joblinks(self,response):
        for jobs in response.css('div[class="job_seen_beacon"]'): 
            job_link=jobs.css('h2[class="jobTitle css-1psdjh5 eu4oa1w0"]').css('a::attr("href")').get()
            yield scrapy.Request('https://www.indeed.com/m'+job_link+'&from=serp',callback=self.parse,headers=self.headers)

        if not response.css('link[rel="next"]::attr("href")').get()==None:
            yield scrapy.Request('https://www.indeed.com'+response.css('link[rel="next"]::attr("href")').get(),headers=self.headers,callback=self.parse_joblinks)
            

    def parse(self,response):
        # breakpoint()
        yield {
            'job_title':response.css('h1[class="jobsearch-JobInfoHeader-title css-1b4cr5z e1tiznh50"]').css('span::text').get(),
            'company_name':response.css("span[class*='jobsearch-JobInfoHeader-companyNameSimple']::text").get() if not response.css("span[class*='jobsearch-JobInfoHeader-companyNameSimple']::text").get()==None else response.css("a[class*='jobsearch-JobInfoHeader-companyNameLink']::text").get(),
            'url':response.url.replace('/m','').replace('&from=serp',''),
            'salary':re.search(r'\$\d{1,3}(?:,\d{3})*(?:\s*-\s*\$\d{1,3}(?:,\d{3})*)?\s*a year', response.text).group() if re.search(r'\$\d{1,3}(?:,\d{3})*(?:\s*-\s*\$\d{1,3}(?:,\d{3})*)?\s*a year', response.text) else 'Not Given',
            # 'job_description':response.css('div#jobDescriptionText').get(),
            'location':response.css('div[data-testid="jobsearch-JobInfoHeader-companyLocation"]').css('span::text').get(),
            'posted_date':re.search(r'"datePosted":"([^"]+)"', response.text).group().replace('\"datePosted\":\"','').replace('\"','') if re.search(r'"datePosted":"([^"]+)"', response.text) else None
        }
            