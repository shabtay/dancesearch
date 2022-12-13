import requests
from bs4 import BeautifulSoup
import csv
import re
from itertools import chain, combinations
import mysql.connector
from dateutil.parser import parse

mydb = mysql.connector.connect(
    host="localhost",
    port="3308",
    user="root",
    password="",
    database="dance_search"
)

dance_types = ['Bachata', 'Salsa', 'Kizomba', 'Brazilian+Zouk']

for dance_type in dance_types:
    URL = f"https://www.danceplace.com//events/in/2023/{dance_type}/-/-"
    r = requests.get(URL)
       
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
        
        print( str(i) + "---------\n" + "URL: " + furl + "\n" + "Name: " + name + "\n" + "Date: " + date + "\n" + "Location: " + location + "\n---------\n" )

        mycursor = mydb.cursor()
        sql = "insert into urls (url, image_url, name, fdate, flocation, dance_type, from_date, to_date, org_name) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = [ furl, img_url, name, date, location, dance_type, from_date, to_date, org_name ]
        mycursor.execute( sql, val )
        url_id = mycursor.lastrowid
        mydb.commit()
