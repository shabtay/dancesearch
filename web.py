import sys
import streamlit as st
import mysql.connector
import re
from dateutil.parser import parse
from urllib.parse import urlparse
import time

import configparser

config = configparser.ConfigParser()
config.sections()
config.read('cnf.ini')

st.set_page_config(
    page_title="Dance Search Engine",
    page_icon = ":shark:"
)

def init_vars():
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1

    if 'glob_term' not in st.session_state:
        st.session_state.glob_term = ""

    
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

    to = st.session_state.page_num * 10
    fr = to - 9
    
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT u.url, u.image_url, u.name, u.dance_type, u.from_date, u.flocation, u.org_name, MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE) AS score FROM urls u WHERE NOW()<from_date and MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE) > 0 ORDER BY `score` DESC, from_date ASC;")
    myresult = mycursor.fetchall()

    mydb.close()

    return( myresult )


def display_results(col1, col2):
    results = st.session_state.results
    displayed = {}

    to = st.session_state.page_num * 10
    fr = to - 9

    if to > len(results):
        to = (int(len(st.session_state.results) / 10) * 10) + len(st.session_state.results) % 10
    
    with col1:
        st.caption(f'**Found {len(st.session_state.results)} results**')
    
    if len(st.session_state.results) > 0:
        with col2:
            st.caption(f'**Display results {fr} - {to}**')
    
    st.write("<hr />", unsafe_allow_html=True)
    
    i = 0
    for item in results:
        i += 1
        if i >= fr and i <= to:
#            if item["url"] not in displayed:
            img = urlparse( item["image_url"] )
            clean_img_url = f"{img.scheme}://{img.netloc}{img.path}"
            with st.container():
                col1, col2 = st.columns([3,7])
                parsed = urlparse(item["url"])
                with col1:
                    st.image(clean_img_url, width=100)
                    st.caption( re.sub(r'[\+]', ' ', item['dance_type']).title() )
                with col2:
                    d = parse(str(item["from_date"])).strftime('%d %b %Y')
                    st.write(f'**Name:** [{item["org_name"].title()}]({item["url"]})')
                    st.write(f'**Date:** {d}')
                    st.write(f'**Location:** {item["flocation"]}')
                    st.caption(f'{parsed.scheme}://{parsed.netloc}')
            
            st.write("<hr />", unsafe_allow_html=True)

def norm_data():
    results = st.session_state.results
    index_to_del = []
    
    i = 0
    while i <= len( results ) - 2:
        j = i + 1
        if ( i not in index_to_del ):
            while j <= len( results ) - 1:
                if results[i]['org_name'] == results[j]['org_name']:
                    results[i]['dance_type'] += f", {results[j]['dance_type']}"
                    index_to_del.insert(0,j)
                j += 1
        i += 1
    
    index_to_del.sort(reverse=True)

    i = 0
    while i < len( index_to_del ):
        item = index_to_del[i]
        i += 1
        results.pop(item)
        
    st.session_state.results = results


def main():
    if 'page_num' not in st.session_state:
        init_vars()

    c1, c2, c3 = st.columns([1,2,1])
    with c1:
        st.write("")
    with c2:
        st.image("latinfest.png", width=300)
    with c3:
        st.write("")
        
    term = st.text_input('**Enter search words:**', placeholder='(ex. "bachata spain", "salsa jan 2023", "madrid", "kizomba may")')
    st.write("")

    if st.session_state.glob_term != term:
        st.session_state.glob_term = term
        st.session_state.page_num = 1
        
        if 'results' in st.session_state:
            del st.session_state.results
        
    if term:
        my_bar = st.progress(0)
        percent_complete = 10
        while percent_complete < 100:
            time.sleep(0.1)
            my_bar.progress(percent_complete)
            percent_complete += 10
            
        my_bar.empty()
        
        col1, col2, col3, col4 = st.columns(4)
        with col3:
            if st.button('Prev', key="prev1"):
                if st.session_state.page_num > 1:
                    st.session_state.page_num -= 1
        with col4:
            if st.button('Next', key="next1"):
                if len(st.session_state.results) % 10 > 0:
                    if st.session_state.page_num + 1 <= int(len(st.session_state.results) / 10) + 1:
                        st.session_state.page_num += 1
                else:
                    if st.session_state.page_num + 1 <= int(len(st.session_state.results) / 10):
                        st.session_state.page_num += 1
                

        if 'results' not in st.session_state:
            st.session_state.results = search(term)
        
        norm_data()
        display_results(col1, col2)


if __name__ == '__main__':
    main()
