import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.fpjourne.com"

response = requests.get(f"{BASE_URL}/en/collections")

soup = BeautifulSoup(response.text, 'html.parser')
watches = {}
watches_count = 0
for link in soup.find_all("a", class_='link magic-carrousel-link'):
    url = BASE_URL + link.get('href')
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = ' '.join(c.strip() for c in soup.find("h1", class_='product-main-title').text.split('\n')[1:7])
    description = soup.find('div', class_='_desc').text.strip()
    images = '\n'.join([src.strip() for src in [img.get('src') for img in soup.findAll('img', class_='img-responsive')]])
    technical_spec = '\n'.join([tech.text.strip('\n').replace('\n', ' ').replace('   ', '').replace(':', ': ') for tech in soup.findAll('div', class_='product-list-specs')[0:2]])
    watches_count = watches_count + 1 
    watches[watches_count] = [url, title, description, images, technical_spec]
    items_df = pd.DataFrame.from_dict(watches, orient='index', columns = ['URL' , 'Title' ,'Description', 'Images', 'Technical Specifications'])
    items_df.to_csv('fpjourne.csv')  