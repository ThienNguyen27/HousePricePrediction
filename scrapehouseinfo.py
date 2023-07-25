from bs4 import BeautifulSoup as bs
import requests
import re

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

my_scraper = Scraper('https://batdongsan.vn/ban-nha/')
houses = my_scraper.info_get()

page = 1
while page != my_scraper.website_pages: 
    if page == 1:
        url = 'https://batdongsan.vn/ban-nha/'
    else: 
        url = f"https://batdongsan.vn/ban-nha/p{page}"
    print(f"trang {page}")

    thien = Scraper(url)
    houses_on_page = thien.info_get()
    for house in houses_on_page:
        print(house)

    page += 1

# mission scrape other info 
