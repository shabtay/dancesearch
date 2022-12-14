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
    
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT DISTINCT(id), u.url, u.image_url, u.name, u.from_date, u.flocation, u.org_name, MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE) AS score FROM urls u WHERE NOW()<from_date and MATCH (name) AGAINST ('{full_term}' IN BOOLEAN MODE) > 0 ORDER BY `score` DESC, from_date ASC;")
    myresult = mycursor.fetchall()

    mydb.close()

    return( myresult )


def display_results( results ):
    displayed = {}

    to = st.session_state.page_num * 10
    fr = to - 9

    st.caption(f'Display results {fr} - {to}')
    
    i = 0
    for item in results:
        i += 1
        if i >= fr and i <= to:
            if item["url"] not in displayed:
                img = urlparse( item["image_url"] )
                clean_img_url = f"{img.scheme}://{img.netloc}{img.path}"
                with st.container():
                    col1, col2 = st.columns([3,7])
                    parsed = urlparse(item["url"])
                    with col1:
                        st.image(clean_img_url, width=100)
                    with col2:
                        st.write(f'**Festival:** [{item["org_name"].title()}]({item["url"]})')
                        st.write(f'**Date:** {item["from_date"]}')
                        st.write(f'**Location:** {item["flocation"]}')
                        st.caption(f'{parsed.scheme}://{parsed.netloc}')
                
                st.write("<hr />", unsafe_allow_html=True)
                displayed[item["url"]] = 1


def main():
    if 'page_num' not in st.session_state:
        init_vars()
        
    st.title( 'Festivals Search Engine' )

    term = st.text_input('Enter search words:')
    
    if st.session_state.glob_term != term:
        st.session_state.glob_term = term
        st.session_state.page_num = 1
        
    if term:
        col1, col2 = st.columns(2)
        with col1:
            if st.button('<<'):
                if st.session_state.page_num > 1:
                    st.session_state.page_num -= 1
        with col2:
            if st.button(f"\>\>"):
                st.session_state.page_num += 1

        results = search(term)
        st.caption(f'Number of results: {len(results)}')
        display_results( results )


if __name__ == '__main__':
    main()
