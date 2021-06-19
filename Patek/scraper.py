import csv
from bs4 import BeautifulSoup
import pandas as pd

with open('PatekPhilippeAllMode.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    wacthes = {}
    wacthes_count = 0
    headers = next(reader)
    for row in reader:
        soup = BeautifulSoup(row[-1:][0], 'html.parser')
        imgs = [img.get('data-src') for img in soup.findAll('img', class_='lazyload')]
        description = row[0]
        watch = row[1]
        dial = row[2]
        case = row[3]
        bracelet = row[4]
        url = row[5]
        for img in imgs:
            wacthes_count = wacthes_count + 1 
            wacthes[wacthes_count] = [description, watch, dial, case, bracelet, url, img]
            items_df = pd.DataFrame.from_dict(wacthes, orient='index', columns = ['Description', 'Watch', 'Dial', 'Case', 'Bracelet', 'URL', 'Image'])
            items_df.to_csv('PatekCleaned.csv')

