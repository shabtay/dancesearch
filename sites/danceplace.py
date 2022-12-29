import requests
from bs4 import BeautifulSoup
import csv
import re
from itertools import chain, combinations
import mysql.connector
from dateutil.parser import parse

def read():
    results = []
    dance_types = ['Bachata', 'Salsa', 'Kizomba', 'Brazilian+Zouk']

    for dance_type in dance_types:
        URL = f"https://www.danceplace.com//events/in/2023/{dance_type}/-/-"

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(URL, headers=headers)
           
        soup = BeautifulSoup(r.content, 'html5lib')
        i = 0

        events_img = soup.findAll('div', attrs = {'class':'event-img'})

        events_html = soup.findAll('div', attrs = {'class':'event-txt'})

        for event_html in events_html:
            i = i + 1
            furl = event_html.find('a', href=True)['href']
            img_url = events_img[i-1].find('img')['src']
            org_name = re.sub(r'[^\w\s]', '', event_html.find('h4').text).lower()
            name = re.sub(r'[^\w\s]', '', event_html.find('h4').text).lower()
            date = event_html.findAll('p')[0].text
            location = event_html.findAll('p')[1].text
            clean_location = re.sub(r'[^\w\s]', '', location).lower()
            
            dates = date.split(' - ')
            from_date = parse(dates[0]).strftime('%Y-%m-%d')
            to_date = parse(dates[1]).strftime('%Y-%m-%d')
            month = parse(dates[1]).strftime('%b')
            full_month = parse(dates[1]).strftime('%B')
            year = parse(dates[1]).strftime('%y')
            full_year = parse(dates[1]).strftime('%Y')

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