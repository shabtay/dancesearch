import sys
import streamlit as st
import mysql.connector

from urllib.parse import urlparse
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('cnf.ini')

st.set_page_config(
    page_title="Dance Search Engine",
    page_icon = ":shark:"
)

def search( full_term ):
    mydb = mysql.connector.connect(
        host = st.secrets['Host'],
        port = st.secrets['Port'],
        user = st.secrets['User'],
        password = st.secrets['Pass'],
        database = st.secrets['DBName']
    )

    terms = full_term.split(' ')
    for i in range(len(terms)):
        terms[i] = terms[i] + "*"
    
    terms_len = len(terms) - 1
    
    full_term = ' '.join(terms)
    
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT DISTINCT(id), u.url, u.image_url, u.name, u.from_date, u.flocation, u.org_name, MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE) AS score FROM urls u where NOW()<from_date and MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE)>={terms_len} ORDER BY `score` DESC, from_date ASC LIMIT 10;")
    myresult = mycursor.fetchall()

    mydb.close()

    return( myresult )

def main():
    st.title('Dance Search Engine')

    term = st.text_input('Enter search words:')
    displayed = {}
    if term:
        results = search(term)
        st.subheader(f'Number of results: {len(results)}')
        for item in results:
            if item["url"] not in displayed:
                img = urlparse( item["image_url"] )
                clean_img_url = f"{img.scheme}://{img.netloc}{img.path}"
                with st.container():
                    col1, col2 = st.columns(2)
                    parsed = urlparse(item["url"])
                    with col1:
                        st.image(clean_img_url, width=100)
                    with col2:
                        st.write(f'**Festival:** [{item["org_name"]}]({item["url"]})')
                        st.write(f'**Website:** {parsed.netloc}')
                        st.write(f'**Date:** {item["from_date"]}')
                        st.write(f'**Location:** {item["flocation"]}')
                
                st.write("<hr />", unsafe_allow_html=True)
                displayed[item["url"]] = 1

if __name__ == '__main__':
    main()
