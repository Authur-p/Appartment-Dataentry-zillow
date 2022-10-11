from pprint import pprint

from selenium import webdriver
from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from bs4 import BeautifulSoup
import requests

header = {
    'Accept-Language': 'en-US;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/103.0.5060.134 Safari/537.36'
}
response = requests.get('https://www.zillow.com/new-york-ny/rentals/2-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A40.917577%2C%22east%22%3A-73.700272%2C%22south%22%3A40.477399%2C%22west%22%3A-74.25909%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%7D'
                        , headers=header)

zillow_web = response.text

soup = BeautifulSoup(zillow_web, 'html.parser')
chrome_driver_path = "D:/New folder/chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

links = soup.select("ul li article a")
prices = soup .select("ul article span")
address = soup.select("ul article address")

all_link = []

for link in links:
    href = link["href"]
    if "http" not in href:
        all_link.append(f"https://www.zillow.com{href}")
    else:
        all_link.append(href)
new_links = [value for idx, value in enumerate(all_link) if idx % 2 == 0]

all_address = [x.text for x in address]
all_prices = [''.join(x.text).split('o')[0] for x in prices]
print(all_prices)

for n in range(len(new_links)):
    driver.get('https://forms.gle/jwpMtnuxJJKqqQwn9')

    sleep(2)

    add = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    pri = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    li = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    add.send_keys(all_address[n])
    pri.send_keys(all_prices[n])
    li.send_keys(new_links[n])
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
    sleep(1)


