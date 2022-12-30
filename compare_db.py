import requests;
import mysql.connector
import tomllib
import logging;
from datetime import date

today = str(date.today())
logging.basicConfig(filename=f'logs\\compare_{today}.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info('Starting process')

with open("secrets.toml", "rb") as f:
    tcnf = tomllib.load(f)


def send_query_to_website( query ):
    url = 'https://latin-fest.com/add_website.php'
    myobj = {'action': 'add_website', 'query': query}
    #print( myobj )
    
    res = requests.post(url, data = myobj)
    print( f"response from server: {res.text}" )
    logging.info( f"response from server: {res.text}" )
    
    if res.text != "0":
        print( f"INFO: website added to latin-fest.com with id {res.text}" )
        logging.info( f"website added to latin-fest.com with id {res.text}" )
    else:
        print( "ERROR: website couldn't added to latin-fest.com" )
        logging.error( "website couldn't added to latin-fest.com" )


mydb = mysql.connector.connect(
    host = tcnf['Host'],
    port = tcnf['Port'],
    user = tcnf['User'],
    password = tcnf['Pass'],
    database = tcnf['DBName']
)

url = 'https://latin-fest.com/add_website.php?action=get_last_id'
res = requests.get(url)
last_server_id = int(res.text)

mycursor = mydb.cursor(dictionary=True)
mycursor.execute( "select max(id) as id from urls" )
myresult = mycursor.fetchall()
last_local_id = int(myresult[0]['id'])

print( f"last server id: {last_server_id} - last local id: {last_local_id}" )
logging.info( f"last server id: {last_server_id} - last local id: {last_local_id}" )

if last_local_id > last_server_id:
    mycursor.execute( f"select * from urls where id > {last_server_id}" )
    myresult = mycursor.fetchall()
    for row in myresult:
        f = ', '.join(row.keys())
        v = ', '.join("'" + str(x).strip() + "'" for x in row.values())
        query = f"insert into urls ({f}) values ({v})"

        print( f"sending {query} to server" )
        logging.info( f"sending {query} to server" )

        send_query_to_website( query )
   