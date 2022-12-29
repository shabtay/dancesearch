import requests
from bs4 import BeautifulSoup
import csv
import re
from itertools import chain, combinations
import mysql.connector
from dateutil.parser import parse

def read():
    results = []
    pages = ['','page/2/']
    dance_types = ['bachata']

    for dance_type in dance_types:
        for page in pages:
            URL = f"https://bachata-embassy.com/festivals/{page}"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.get(URL, headers=headers)
               
            soup = BeautifulSoup(r.content, 'html5lib')
                
            i = 0

            events_html = soup.findAll('div', attrs = {'class':'event_listing'})
            for event_html in events_html:
                furl = event_html.find('a', attrs = {'class':'wpem-event-action-url'}, href=True)['href']
                img_url = re.search("https.*?\s", event_html.find('div', attrs = {'class':'wpem-event-banner-img'})['style'] ).group().strip()
                org_name = event_html.find('h3', attrs = {'class':'wpem-heading-text'}).text
                name = re.sub(r'[^\w\s]', '', org_name).lower()
                date = event_html.find('span', attrs = {'class':'wpem-event-date-time-text'}).text
                location = event_html.find('span', attrs = {'class':'wpem-event-location-text'}).text.strip()
                clean_location = re.sub(r'[^\w\s]', '', location).lower()

                dates = date.split(' - ')
                from_date = parse(dates[0]).strftime('%Y-%m-%d')
                to_date = parse(dates[1]).strftime('%Y-%m-%d')
                month = parse(dates[0]).strftime('%b')
                full_month = parse(dates[0]).strftime('%B')
                year = parse(dates[0]).strftime('%y')
                full_year = parse(dates[0]).strftime('%Y')

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
