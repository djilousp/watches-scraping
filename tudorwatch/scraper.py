
import requests
import pandas as pd
from termcolor import colored
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, element

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors') 
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

watches = {}
watches_count = 0
baseUrl = "https://www.tudorwatch.com/en/watches"
driver.get(baseUrl)
driver.implicitly_wait(10)
try: 
    button = driver.find_element_by_css_selector(".sc-llYToB")
    while True:
        button.click()
        try:
            button = driver.find_element_by_css_selector(".sc-llYToB")
        except:
            break

    a_tags = driver.find_elements_by_css_selector(".sc-cvZATX")
    for a in a_tags:
        url = a.get_attribute('href')
        res = requests.get(url)
        print(f'Scrapping URL : ' + url)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = ' : '.join([t.text for t in soup.findAll('a', class_='breadcrumb-link')[2:4]])
        elements = soup.find('div', class_='watchspecifications').findChildren('li')
        specs = '\n'.join([e.findChildren("h3")[0].text + " : " + e.findChildren("p")[0].text for e in elements if len(e.findChildren("h3")) and len(e.findChildren("p"))])
        watches_count = watches_count + 1 
        watches[watches_count] = [url, title, specs]
        items_df = pd.DataFrame.from_dict(watches, orient='index', columns = ['URL' , 'Title', 'Specifications'])
        items_df.to_csv('tudor.csv')  
        print('------------------------------------------------------------------------------------------------------------')
except:
    print("Something went wrong run the scrapper again please.")



