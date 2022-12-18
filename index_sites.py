import mysql.connector
import configparser
import tomllib
import logging
from datetime import date

import sites.goandance as gad
import sites.bembassy as bb
import sites.danceplace as dp
import sites.latindancecal as ldc


config = configparser.ConfigParser()
config.sections()
config.read('cnf.ini')

with open("secrets.toml", "rb") as f:
    tcnf = tomllib.load(f)

today = str(date.today())
logging.basicConfig(filename=f'logs\\app_{today}.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info('Starting process')

def write_results_to_db( res ):
    print( f"Loading current URLs from DB" )
    logging.info( f"Loading current URLs from DB" )
    current_urls = {}
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT u.url FROM urls u;")
    myresult = mycursor.fetchall()
    for url in myresult:
        current_urls[url['url']] = 1

    print( f"Load {len(current_urls)} records from DB" )
    logging.info( f"Load {len(current_urls)} records from DB" )
        
    counter = 0
    adding = 0
    for site in res:
        for record in site:
            counter += 1
            mycursor = mydb.cursor()
            sql = "insert into urls (url, image_url, name, fdate, flocation, dance_type, from_date, to_date, org_name) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = [ 
                record['url'], 
                record['img_url'], 
                record['name'], 
                record['date'], 
                record['location'], 
                record['dance_type'], 
                record['from_date'], 
                record['to_date'], 
                record['org_name'] 
            ]
            
            if record['url'] not in current_urls:
                adding += 1
                print( f"{counter}) Adding {record['org_name']} - {record['url']} to db" )
                logging.info( f"{counter}) Adding {record['org_name']} - {record['url']} to db" )
                mycursor.execute( sql, val )
                mydb.commit()
                current_urls[record['url']] = 1
    
    print( f"{adding}/{counter} records added to DB" )
    logging.info( f"{adding}/{counter} records added to DB" )


mydb = mysql.connector.connect(
    host = tcnf['Host'],
    port = tcnf['Port'],
    user = tcnf['User'],
    password = tcnf['Pass'],
    database = tcnf['DBName']
)

res = []
print( 'Collecting records from Goandance' )
logging.info( 'Collecting records from Goandance' )
if config['SITES']['Goandance'] == "1" : 
    sres = gad.read()
    print( f'Got {len(sres)} records from Goandance' )
    logging.info( f'Got {len(sres)} records from Goandance' )
    res.append( sres )

print( 'Collecting records from Bembassy' )
logging.info( 'Collecting records from Bembassy' )
if config['SITES']['Bembassy'] == "1" : 
    sres = bb.read()
    print( f'Got {len(sres)} records from Bembassy' )
    logging.info( f'Got {len(sres)} records from Bembassy' )
    res.append( sres )

print( 'Collecting records from Danceplace' )
logging.info( 'Collecting records from Danceplace' )
if config['SITES']['Danceplace'] == "1" : 
    sres = dp.read()
    print( f'Got {len(sres)} records from Danceplace' )
    logging.info( f'Got {len(sres)} records from Danceplace' )
    res.append( sres )

print( 'Collecting records from Latindancecal' )
logging.info( 'Collecting records from Latindancecal' )
if config['SITES']['Latindancecal'] == "1" : 
    sres = ldc.read()
    print( f'Got {len(sres)} records from Latindancecal' )
    logging.info( f'Got {len(sres)} records from Latindancecal' )
    res.append( sres )

write_results_to_db( res )

mydb.close()
