import requests
from bs4 import BeautifulSoup
import csv
import re
from itertools import chain, combinations
import mysql.connector
from dateutil.parser import parse

def read():
    results = []
    dance_types = ['bachata', 'salsa', 'kizomba', 'zouk']

    for dance_type in dance_types:
        URL = f"https://latindancecalendar.com/festivals/location/europe/style/{dance_type}/"
        r = requests.get(URL)
           
        soup = BeautifulSoup(r.content, 'html5lib')
            
        i = 0

        events_html = soup.findAll('div', attrs = {'class':'vevent'})
        #print( f"{dance_type} : {len(events_html)}" )
        for event_html in events_html:
            furl = event_html.find('a', attrs = {'class':'inbound festivals link'}, href=True)['href']
            img_url = event_html.find('img', attrs = {'class':'photo'})['src']
            org_name = event_html.find('a', attrs = {'class':'inbound festivals link'}).text #re.sub(r'[^\w\s]', '', event_html.find('h4').text).lower()
            name = re.sub(r'[^\w\s]', '', org_name).lower()
            date = event_html.find('span', attrs = {'class':'value-title'})['title']
            location = event_html.find('span', attrs = {'class':'location'}).text
            clean_location = re.sub(r'[^\w\s]', '', location).lower()

            
            # dates = date.split(' - ')
            from_date = parse(date).strftime('%Y-%m-%d')
            to_date = parse(date).strftime('%Y-%m-%d')
            month = parse(date).strftime('%b')
            full_month = parse(date).strftime('%B')
            year = parse(date).strftime('%y')
            full_year = parse(date).strftime('%Y')

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
