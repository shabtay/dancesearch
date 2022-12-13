import sys
import streamlit as st
import mysql.connector

from urllib.parse import urlparse
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('cnf.ini')

def search( full_term ):
    mydb = mysql.connector.connect(
        host = config['DB']['Host'],
        port = config['DB']['Port'],
        user = config['DB']['User'],
        password = config['DB']['Pass'],
        database = config['DB']['DBName']
    )

    terms = full_term.split(' ')
    for i in range(len(terms)):
        terms[i] = terms[i] + "*"
        
    full_term = ' '.join(terms)
    
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT DISTINCT(id), u.url, u.image_url, u.name, u.from_date, u.flocation, u.org_name, MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE) AS score FROM urls u where NOW()<from_date and MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE)>0 ORDER BY `score` DESC, from_date ASC;")
    myresult = mycursor.fetchall()

    mydb.close()

    return( myresult )

def main():
    st.title('Dance Search Engine')
    term = st.text_input('Enter search words:')
    displayed = {}
    if term:
        results = search(term)
        st.write(f'<p>Number of results: {len(results)}</p><br />', unsafe_allow_html=True)
        for item in results:
            if item["url"] not in displayed:
                parsed = urlparse(item["url"])
                st.write(
                    f'<div class="res"><img style="width:50px; height:50px" src="{item["image_url"]}"/> \
                    <a href="{item["url"]}">{item["org_name"]}</a><br /> \
                    <div>Website: {parsed.netloc}</div><div>StartDate: {item["from_date"]}</div><div>Location: {item["flocation"]}</div></div><hr />', unsafe_allow_html=True)
                displayed[item["url"]] = 1

if __name__ == '__main__':
    main()