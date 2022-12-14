import mysql.connector
import configparser
import tomllib

import sites.goandance as gad
import sites.bembassy as bb
import sites.danceplace as dp
import sites.latindancecal as ldc

config = configparser.ConfigParser()
config.sections()
config.read('cnf.ini')

with open("secrets.toml", "rb") as f:
    tcnf = tomllib.load(f)

def write_results_to_db( res ):
    current_urls = {}
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT u.url FROM urls u;")
    myresult = mycursor.fetchall()
    for url in myresult:
        current_urls[url['url']] = 1
        
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
                mycursor.execute( sql, val )
                mydb.commit()
    
    print( f"{adding}/{counter} records added to DB" )


mydb = mysql.connector.connect(
    host = tcnf['Host'],
    port = tcnf['Port'],
    user = tcnf['User'],
    password = tcnf['Pass'],
    database = tcnf['DBName']
)

res = []
print( 'Collecting records from Goandance' )
if config['SITES']['Goandance'] == "1" : res.append( gad.read() )

print( 'Collecting records from Bembassy' )
if config['SITES']['Bembassy'] == "1" : res.append( bb.read() )

print( 'Collecting records from Danceplace' )
if config['SITES']['Danceplace'] == "1" : res.append( dp.read() )

print( 'Collecting records from Latindancecal' )
if config['SITES']['Latindancecal'] == "1" : res.append( ldc.read() )

write_results_to_db( res )

mydb.close()
