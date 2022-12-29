import requests
from bs4 import BeautifulSoup
import csv
import re
from itertools import chain, combinations
import mysql.connector
from dateutil.parser import parse

def read():
    results = []
    dance_types = {'bachata':'18%2C3%2C16','salsa':'19%2C20%2C2%2C48%2C15%2C13%2C21%2C9%2C12%2C1%2C14%2C10%2C11','kizomba':'4%2C41%2C22%2C23%2C52','zouk':'8%2C51%2C49'}

    for dance_type in dance_types:
        next_page = ""
        page = 0
        while next_page != "-1":
            URL = f"https://www.goandance.com/en/events/festivals/{next_page}?style={dance_types[dance_type]}"
            #print( URL )
            
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(URL, headers=headers)
               
            soup = BeautifulSoup(r.content, 'html5lib')
        
            next_page_icon = soup.find('span', attrs = {'class':'fa fa-chevron-right'})
            if next_page_icon is None:
                next_page = "-1"
            else:
                page = page + 1
                next_page = str(page)
            
            i = 0
            events_html = soup.findAll('div', attrs = {'class':'event-item'})
     
            for event_html in events_html:
                furl = event_html.find('meta', attrs = {'itemprop':'url'})['content']
                img_url = event_html.find('img', attrs = {'class':'img-responsive lazy-load'})['src']
                org_name = event_html.find('span', attrs = {'itemprop':'name'}).text.strip()
                name = re.sub(r'[^\w\s]', '', org_name).lower()
                start_date = event_html.find('meta', attrs = {'itemprop':'startDate'})['content']
                end_date = event_html.find('meta', attrs = {'itemprop':'endDate'})['content']

                addressRegion = event_html.find('meta', attrs = {'itemprop':'addressRegion'})['content']
                country = event_html.find('meta', attrs = {'itemprop':'addressCountry'})['content']
                location = f"{addressRegion} {country}"
                clean_location = re.sub(r'[^\w\s]', '', location).lower()

                from_date = parse(start_date).strftime('%Y-%m-%d')
                to_date = parse(end_date).strftime('%Y-%m-%d')
                date = f"{from_date} - {to_date}"
                month = parse(from_date).strftime('%b')
                full_month = parse(from_date).strftime('%B')
                year = parse(from_date).strftime('%y')
                full_year = parse(from_date).strftime('%Y')

                if name.find( dance_type.lower() ) == -1:
                    clean_dance_type = re.sub(r'[^\w\s]', '', dance_type.lower())
                    name = name + f" {clean_dance_type}"
                
                name = name + f" {month}"
                
                if name.find( full_month.lower() ) == -1:
                    name = name + f" {full_month}"
                
                name = name + f" {year}"
                
                if name.find( full_year.lower() ) == -1:
                    name = name + f" {full_year}"
                
                name = name + f" {clean_location}"

                #print( f"---------\nURL: {furl}\nName: {name}\nDate: {from_date} - {to_date}\nLocation: {location}\n---------\n" )
                results.append({
                    'url': furl,
                    'img_url': img_url,
                    'name': name,
                    'date': date,
                    'location': location,
                    'dance_type': dance_type,
                    'from_date': from_date,
                    'to_date': to_date,
                    'org_name': org_name
                })
    
    return( results )
