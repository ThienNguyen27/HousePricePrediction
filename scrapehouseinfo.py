# Using bs to scrape data
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import threading
# information for house: price, area, number of toilet, number of bedroom, location, no of floor

page = 1 
website_pages = 7
thread_num = 6
data = []
threads = []

# Construction of the Scaper bot
class Scaper:
    def __init__(self, url):
        self.html = requests.get(url)
    
    def info_get(self):
        self.raw_info = bs(self.html.text, 'html.parser')
        self.data_list = self.raw_info.find('div', class_ = 'datalist')
        self.list=[]
        for name_list in self.data_list.find_all('div', class_ = 'name'):
            for link in name_list.find_all('a', attrs = {'href': re.compile("^https://")}):
                self.list.append(link.get('href'))
        return self.list

    
if __name__ == "__main__":
    while page != website_pages: 
        if page == 1:
            url = 'https://batdongsan.vn/ban-nha/'
        else: 
            url = f"https://batdongsan.vn/ban-nha/p{page}"
        print(f"trang {page}")

        # scrape house price and area by their span classes
        
        thien = Scaper(url)
        data.append(thien.info_get())

        page += 1
    print(data)



# tạo list của các nhà, mỗi nhà là một dictionary

# list_of_house = []
