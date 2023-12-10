countingpage_scraper = Scraper('https://batdongsan.vn/ban-nha/')
houses = countingpage_scraper.url_get()
url_list = []
page = 1

starting_time = time.time()
print("Start getting url")

while page != 26:
    if page == 1:
        url = 'https://batdongsan.vn/ban-nha/'
    else:
        url = f"https://batdongsan.vn/ban-nha/p{page}"
    print(f"trang {page}")

    house_scraper = Scraper(url)
    houses_on_page = house_scraper.url_get() # Get House_url

    for house_url in houses_on_page:
        url_list.append(house_url)

    page += 1

finishing_time = time.time()
print(f"Time to complete getting url: {finishing_time - starting_time}s")
# print(len(url_list))
# print(url_list)
# Start crawling through the url lists
house_data = Scraper_thread(url_list)

# create df and store file csv in the local device
import pandas as pd

df = pd.DataFrame(house_data)
df.to_csv('house.csv')
