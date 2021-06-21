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
    images = [src.strip() for src in [img.get('src') for img in soup.findAll('img', class_='img-responsive')]]
    titles = [title.text.strip('\n').replace('\n', ' ').replace('   ', '').replace(' :', '').strip() for title in soup.findAll('div', class_='_title')[0:2]]
    #technical_spec = [tech.text.strip('\n').replace('\n', ' ').replace('   ', '').replace(':', ': ') for tech in soup.findAll('div', class_='product-list-specs')]
    specs = [spec.text.strip('\n').replace('\n', ' ').replace('   ', '').replace(':', ': ').strip()  for spec in soup.findAll('ul', class_='_list')[0:2]]
    # first_spec = technical_spec[0].split(":")[0].strip()
    # second_spec = technical_spec[1].split(":")[0].strip()
    # first_desc = ":".join(technical_spec[0].split(":")[1:-1]).strip()
    # second_desc = ":".join(technical_spec[1].split(":")[1:-1]).split("mm")[0].strip() + " mm"
    # if (first_spec != 'Movement'):
    #     first_desc = ""
    
    titles_specs = dict(zip(titles, specs))
    movement_desc = titles_specs['Movement'] if 'Movement' in titles_specs.keys() else ''
    dimensions_desc = titles_specs['Dimensions'] if 'Dimensions' in titles_specs.keys() else ''

    for image in images:
        watches_count = watches_count + 1 
        watches[watches_count] = [url, title, description, image, movement_desc, dimensions_desc]
        items_df = pd.DataFrame.from_dict(watches, orient='index', columns = ['URL' , 'Title' ,'Description', 'Image', 'Movement', 'Dimensions'])
        items_df.to_csv('fpjourne.csv')  