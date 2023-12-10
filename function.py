from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd
import time
import concurrent.futures
import os
from concurrent.futures import ThreadPoolExecutor

class Scraper():
    def __init__(self, url):
        self.html = requests.get(url)
        self.raw_info = bs(self.html.text, 'lxml') #################################
        self.data_in_page = self.raw_info.find('div', class_='datalist')
        self.housing_records = int(self.raw_info.strong.string.replace(",", ""))
        self.website_pages = self.housing_records // 20 + 1
        self.house_list = []

    def url_get(self):
      if self.data_in_page:
        for name_list in self.data_in_page.find_all('div', class_='name'):
            link = name_list.find('a', href=re.compile("^https://"))
            if link:
              self.house_list.append(link.get('href'))
        return self.house_list
      else:
        print("Element 'data_in_page' not found")
# Processing price string
def replace_money_unit(txt: str):
  global value
  if "triệu" in txt.lower():
    value = float(txt.lower().replace(' triệu',''))*(10**6)
  elif "tỷ" in txt.lower():
    value = float(txt.lower().replace(' tỷ',''))*(10**9)
  else:
    value = txt
  return value

def data_get(url):
    house_data ={}
  # Scrape price, area, bedrooms, toilet, and location, news for each house URL
    house_response = requests.get(url)
    house_info = bs(house_response.text, 'lxml') ###################################

    # Url
    house_data['url'] = url

    # Price
    price = house_info.find("strong", class_="price")
    if price:
      price_string = price.text.strip()
      new_price = replace_money_unit(price_string)
      house_data['price'] = new_price

    # Area
    area = house_info.find("strong", string="Diện tích:")
    if area:
      house_data['area'] = float(area.next_sibling.string.strip("m"))


    # Bedrooms
    bedrooms = house_info.find("strong", string="Phòng ngủ:")
    if bedrooms:
      house_data['bedrooms'] = int(bedrooms.next_sibling.string.strip("PN"))

    # Toilet
    toilet = house_info.find("strong", string="Phòng WC:")
    if toilet:
      house_data['toilets'] = int(toilet.next_sibling.string.strip("WC"))

    # Location
    location_item = house_info.find("ul", class_="uk-breadcrumb")
    if location_item:
        location_list = location_item.find_all("li")
        if location_list:
          house_data['location'] = location_list[len(location_list) - 2].text
        else:
          print("No 'li' elements found within 'ul' with class 'uk-breadcrumb'")
    else:
      print("No 'ul' element with class 'uk-breadcrumb' found")

    # News
    news = house_info.find("div", class_ = "content")
    if news:
      description = news.text.replace("\r\n"," ").replace("\n"," ")
      house_data['news'] = description
      try:
        level_string = re.search('[0-9]{1,2} tầng|[0-9]{1,2}tầng|[0-9]{1,2}tầng', description.lower()).group()
        levels = re.search('[0-9]{1,2}', level_string).group()
        house_data['level']= int(levels)
      except AttributeError:
        try:
          level_string = re.search('[0-9]{1,2} lầu|[0-9]{1,2}lầu', description.lower()).group()
          levels = re.search('[0-9]{1,2}', level_string).group()
          house_data['level'] = int(levels) + 1
        except AttributeError:
          print('Missing level')
      if not area:
        try:
          area_string= re.search('[0-9]{1,2}m2|[0-9]{1,2} m2|diện tích: [0-9]{1,2}|dt:[0-9]{1,2}|[0-9]{1,2}m²|[0-9]{1,2} m²', description.lower()).group()
          area = float(re.search("[0-9]{1,2}", area_string).group())
          house_data['area'] = area
        except:
          try:
            size = re.search('[0-9]{1,2}x[0-9]{1,2}',description.lower()).group()
            side1_string = re.search('[0-9]{1,2}x', size).group()
            side1 = float(side1_string[0:len(side1_string)-1])
            side2_string = re.search('x[0-9]{1,2}', size).group()
            side2 = float(side2_string[1:])
            house_data['area'] = side1 * side2
          except:
            print('Missing area')
      if not bedrooms:
        try:
          bedroom_string = re.search('[0-9]{1,2}pn|[0-9]{1,2} pn|[0-9]{1,2}phòng ngủ|[0-9]{1,2} phòng ngủ|[0-9]{1,2} ngủ|[0-9]{1,2}ngủ', description.lower()).group()
          bedroom = int(re.search('[0-9]{1,2}',bedroom_string).group())
          house_data['bedrooms'] = bedroom
        except:
          print("Missing bedroom")

      if not toilet:
        try:
          toilet_string = re.search('[0-9]{1,2}wc|[0-9]{1,2} wc|[0-9]{1,2}vệ sinh|[0-9]{1,2} vệ sinh|[0-9]{1,2}toilet|[0-9]{1,2} toilet|[0-9]{1,2} nhà vệ sinh|[0-9]{1,2}nhà vệ sinh|[0-9]{1,2}tolet|[0-9]{1,2} tolet', description.lower()).group()
          toilet = int(re.search('[0-9]{1,2}',toilet_string).group())
          house_data['toilets'] = toilet
        except:
          print('Missing toilet')
    return house_data
def Scraper_thread(urls: list):
    house_data = []
    starting_time = time.time()
    print("Start Scraping")
    with ThreadPoolExecutor(max_workers=1000) as executor:##############################
      results = executor.map(data_get, urls, chunksize=8)###############################
      executor.shutdown()###############################################################
    house_data = [house for house in results]###########################################

    finishing_time = time.time()
    print(house_data)
    print("Scraping finished")
    print(f"Time to complete Scraping: {finishing_time - starting_time}s")
    return house_data
