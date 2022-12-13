import mysql.connector
import configparser

import sites.goandance as gad
import sites.bembassy as bb
import sites.danceplace as dp
import sites.latindancecal as ldc

config = configparser.ConfigParser()
config.sections()
config.read('cnf.ini')

def write_results_to_db( res ):
    counter = 0
    for site in res:
        for record in site:
            counter = counter + 1
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
            
            print( f"{counter}) Adding {record['org_name']} to db" )
            mycursor.execute( sql, val )
            mydb.commit()
    
    print( f"{counter} records added to DB" )


mydb = mysql.connector.connect(
    host = config['DB']['Host'],
    port = config['DB']['Port'],
    user = config['DB']['User'],
    password = config['DB']['Pass'],
    database = config['DB']['DBName']
)

res = []
if config['SITES']['Goandance'] == "1" : res.append( gad.read() )
if config['SITES']['Bembassy'] == "1" : res.append( bb.read() )
if config['SITES']['Danceplace'] == "1" : res.append( dp.read() )
if config['SITES']['Latindancecal'] == "1" : res.append( ldc.read() )

write_results_to_db( res )

mydb.close()
