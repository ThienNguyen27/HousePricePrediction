from bs4 import BeautifulSoup as bs
import requests
import re
import threading
import concurrent.futures
import logging

# information for house: price, area, number of toilet, number of bedroom, location, no of floor

https://github.com/ThienNguyen27/HousePricePrediction/pull/1/conflict?name=scrapehouseinfo.py&ancestor_oid=aed49e895af5485e5131e7ed5cf69617d9befbfc&base_oid=55ea3bcaa436d934a17f97f4d280542600f48a7a&head_oid=6d00c9b64e1df4efded4e4fbf0a914e6b67e6487#Constances
page = 1 
website_pages = 7
thread_num = 6
landing_url = 'https://batdongsan.vn/ban-nha/'
data = []

# Construction of the Scaper bot
class Scraper():
    def __init__(self, url):
        self.html = requests.get(url)
        self.raw_info = bs(self.html.text, 'html.parser')
        self.data_list = self.raw_info.find('div', class_='datalist')
        Housing_records = int(self.raw_info.strong.string.replace(",", ""))
        self.website_pages = Housing_records // 20 + 1  
        self.house_list = []

    def info_get(self):
        for name_list in self.data_list.find_all('div', class_='name'):
            house_data = {} # Using the dictionary extract other information such as price, area, bedrooms, etc.
            link = name_list.find('a', href=re.compile("^https://"))
            if link:
                house_data['url'] = link.get('href')
                self.house_list.append(house_data)
        return self.house_list


Chithien = Scraper(landing_url)



houses = Chithien.info_get()
thien = Scraper(landing_url)
page = 1

if __name__ == "__main__": 
    while page != Chithien.website_pages: 
        if page == 1:
            url = 'https://batdongsan.vn/ban-nha/'
        else: 
            url = f"https://batdongsan.vn/ban-nha/p{page}"
        print(f"trang {page}")


            
        houses_on_page = thien.info_get()
        # for house in houses_on_page:
        #     print(house)


        page += 1

