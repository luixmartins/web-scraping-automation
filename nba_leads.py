from selenium import webdriver
from selenium.webdriver.edge.options import Options

from bs4 import BeautifulSoup as bs 
import pandas as pd 

from datetime import datetime

try: 
    options = Options()
    options.add_argument("--headless")
    
    driver = webdriver.Edge(options=options)
    
    driver.get("https://www.nba.com/stats/leaders")

    element = driver.find_element(by="xpath", value="/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]")

    html = element.get_attribute('outerHTML')
    driver.quit()

except Exception as e:
    print(e)

soup = bs(html, 'html.parser')

head = []

head_tr = soup.find("tr", {"class": "Crom_headers__mzI_m"})

for tr in head_tr: 
    head.append(tr.get_text().strip())


table_rows = soup.find("tbody").find_all("tr")

table_data = []

for row in table_rows: 
    cols = row.find_all("td")
    cols = [element.text.strip() for element in cols]
    
    table_data.append([element for element in cols if element])


df = pd.DataFrame(table_data, columns=head) 

df.set_index('#', inplace=True)

date = datetime.today().strftime('%Y-%m-%d') 

path = f'datasets/nba-leads-{date}.csv'

df.to_csv(path)