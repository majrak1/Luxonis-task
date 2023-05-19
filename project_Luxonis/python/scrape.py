import scrapy
from scrapy.crawler import CrawlerProcess
import json
import requests
import mysql.connector


class SrealitySpider(scrapy.Spider):
    # Spider initialization
    name = 'srealitypage'
    allowed_domains = ['sreality.cz']
    start_urls = ['https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&per_page=60&tms=1682525807015']
    

    def parse(self, response):
        base_url = 'https://www.sreality.cz/api/en/v2/estates'
        params = {'category_main_cb': '1', 'category_type_cb': '1', 'per_page': '60', 'tms': '1682525807015'}
        count = 0
        loop = True
        page_num = 1

        # search for first 500 items
        while loop:
            params['page'] = page_num
            response = requests.get(base_url, params=params)
            # search for items in the response
            data = json.loads(response.text)
                        
            for item in data['_embedded']['estates']:
                # checks if the count is 500
                if count >= 500:
                    loop = False
                else:
                    count += 1                
                
                # find image url
                estate_images = item['_links']
                for estate_image in estate_images:
                    estate_image = estate_images['dynamicDown']
                    for d in estate_image:
                        image_href = d['href']                        
                        url = image_href.split('=res')[0] + '=res'
                        url.replace('fl=res', "")
                        url += ",400,300,3|shr,,20|jpg,90"
                
                # upload data to the database
                connection = mysql.connector.connect(
                    user='root', password='root', host='mysql', port="3306", database='db')
                print("DB connected")

                cur = connection.cursor()                            

                cur.execute("""
                    INSERT INTO apartment (title, url)
                    VALUES (%s, %s)
                """, (item['name'], url))                

                connection.commit()
                cur.close()
                connection.close()                
            page_num += 1
            


# Start the crawler
process = CrawlerProcess()
process.crawl(SrealitySpider)
process.start()




