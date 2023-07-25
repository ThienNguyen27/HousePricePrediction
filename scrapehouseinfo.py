# Using bs to scrape data
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
# information for house: price, area, number of toilet, number of bedroom, location, no of floor

page = 1 
website_pages = 2
Price_area_list=[]
while page != website_pages: 
    if page == 1:
        url = 'https://batdongsan.vn/ban-nha/'
    else: 
        url = f"https://batdongsan.vn/ban-nha/p{page}"
    print(f"trang {page}")

    # scrape house price and area by their span classes
    html = requests.get(url) 
    Scraped_rawinfo = bs(html.text, 'html.parser')
    data_list = Scraped_rawinfo.find('div', class_ = 'datalist')  
    # prices = Scraped_rawinfo.find_all('span', {'class': 'price'})
    # areas = Scraped_rawinfo.find_all('span', {'class': 'acreage'})
    # for price in prices:
    #     print(price.string.strip())
    # for area in areas:
    #     print(area.text.strip('m2')) # eliminate area units  
    
    for name_list in data_list.find_all('div', class_ = 'name'):
        for link in name_list.find_all('a', attrs={'href': re.compile("^https://")}):
    # display the actual urls
            print(link.get('href'))
    page += 1



# print(Price_area_list)

# tạo list của các nhà, mỗi nhà là một dictionary

# list_of_house = []
