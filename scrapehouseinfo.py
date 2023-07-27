from bs4 import BeautifulSoup as bs
import requests
import re

class Scraper():
    def __init__(self, url):
        self.html = requests.get(url)
        self.raw_info = bs(self.html.text, 'html.parser')
        self.data_in_page = self.raw_info.find('div', class_='datalist')
        self.housing_records = int(self.raw_info.strong.string.replace(",", ""))
        self.website_pages = self.housing_records // 20 + 1  
        self.house_list = []

    def url_get(self):
        for name_list in self.data_in_page.find_all('div', class_='name'):
            house_data = {} # Using the dictionary extract other information such as price, area, bedrooms, etc.
            link = name_list.find('a', href=re.compile("^https://"))
            if link:
                house_data['url'] = link.get('href')
                self.house_list.append(house_data)
        return self.house_list

    def data_get(self):
        for name_list in self.data_in_page.find_all('div', class_='name'):
            house_data = {}  # Using the dictionary to extract other information such as price, area, bedrooms, etc.
            link = name_list.find('a', href=re.compile("^https://"))
            if link:
                house_data['url'] = link.get('href')

                # Scrape price, area, bedrooms, toilet, and location, news for each house URL
                house_response = requests.get(house_data['url'])
                house_info = bs(house_response.text, 'html.parser')
                
                # Price
                price = house_info.find("strong", class_="price")
                house_data['price']= price.text.strip() if price else "N/A"
                # Area
                area = house_info.find("strong", string="Diện tích:")
                house_data['area'] = area.next_sibling.string.strip("m") if area else "N/A"

                # Bedrooms
                bedrooms = house_info.find("strong", string="Phòng ngủ:")
                house_data['bedrooms'] = bedrooms.next_sibling.string.strip("PN") if bedrooms else "N/A"

                # Toilet
                toilet = house_info.find("strong", string="Phòng WC:")
                house_data['toilets'] = toilet.next_sibling.string.strip("WC") if toilet else "N/A"

                # Location
                location_item = house_info.find("ul", class_="uk-breadcrumb").find_all("li") 
                location = []
                for i in range(2, len(location_item)):
                    location.append(location_item[i].text) 
                house_data['location'] = location if location_item else "N/A"
                self.house_list.append(house_data)

                # News
                news = house_info.find("div", class_ = "content")
                house_data['news'] = news.text.replace("\r\n"," ").replace("\n"," ")

        return self.house_list

countingpage_scraper = Scraper('https://batdongsan.vn/ban-nha/') 
houses = countingpage_scraper.url_get() 


url_list = []
page = 1
# while page != countingpage_scraper.website_pages: 
while page != 6:
    if page == 1:
        url = 'https://batdongsan.vn/ban-nha/'
    else: 
        url = f"https://batdongsan.vn/ban-nha/p{page}"
    print(f"trang {page}")
    
    house_scraper = Scraper(url)
    houses_on_page = house_scraper.data_get()
    

    for house in houses_on_page:
        print(house)
        

    page += 1


#Start threading

# mission scrape other info 
