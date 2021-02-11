
# This code is to scrape the connection details of a Netgear CM1000v2 Cable Modem.

print('Script Start')

##### Bring in the modules needed to run things.
import sys
import requests
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler
import mysql.connector
from mysql.connector import Error

##### Setting up Logging
gv_logpath = 'status.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(gv_logpath, mode='a', maxBytes=50*1024, backupCount=1, encoding=None, delay=0)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


##### Scraping the Modem page for the details needed. 
def Scrape():

    ########## User Configuration
    
    # Router Login
    gv_username = 'CMUSERNAME'
    gv_password = 'CMPASSWORD'
    
    
    ########## MySQL Server Connection Details and Configuration
    try:
        conn = mysql.connector.connect(
          host='DBSERVER_ADDRESS',
          user='DBUSER',
          password='DMPASSWORD',
          database='YOURDB'
          )
    
        if conn.is_connected():
            print('Connected to MySQL')
            logger.info('Connected to MySQL')
            cur = conn.cursor()
    
    except Error as e:
        print('Error while connecting to MySQL: ' + e)
        logger.info('Error while connecting to MySQL: ' + e)
    
    finally:
        if (conn.is_connected()):
    
            # Processing the Webpage    
            #Reading the Status page of the modem.
            logger.info('Reading the Webpage')
            print('Reading the Webpage')
            response = requests.get("http://192.168.100.1/DocsisStatus.asp", auth=(gv_username, gv_password))
            content = response.text
            soup = BeautifulSoup(content,'lxml')
    
    
            # Returns the System Time
            def SysTime():
                logger.info('Getting the System Time')
                print('Getting the System Time')
                for systime in soup.find_all('td', id='Current_systemtime'):
                    time = systime.text.replace('Current System Time:', '').strip()
                    return time
    
            # Returns the time since last reboot
            def SysUpTime():
                logger.info('Getting the Up Time')
                print('Getting the Up Time')
                for sysuptime in soup.find_all('td', id='SystemUpTime'):
                    uptime = sysuptime.text.replace('System Up Time:', '').strip()
                    return uptime
    
            # Scraping the data to return the tables
            def ProcessTable(def_tbl_id):
                logger.info('Parsing a Table')
                print('Parsing a Table')
                tabledetails = []
                for table in soup.find_all('table', id=def_tbl_id):
                    for row in table.find_all('tr'):
                        for detail in row.find_all('td'):
                            clean_detail = detail.text.strip()
                            tabledetails.append(clean_detail)
                return tabledetails
    
                        
            # Using the Functions
            pulltime = SysTime()
            uptime = SysUpTime()
            downstream = ProcessTable('dsTable')
            upstream = ProcessTable('usTable')
            downstreamOFDMA = ProcessTable('d31dsTable')
            upstreamOFDMA = ProcessTable('d31usTable')
               
            return conn, cur, pulltime, uptime, downstream, upstream, downstreamOFDMA, upstreamOFDMA


# Dealing with bad Scrapes.
# If there is a bad scrape the system will try again.
finished = False

while not finished:
    conn, cur, pulltime, uptime, downstream, upstream, downstreamOFDMA, upstreamOFDMA = Scrape()
    checkresult = isinstance(pulltime,str)
    if checkresult == True:
        finished = True
        

##### This breaks a list at a given length and then loops
def DivideList(def_list,def_chunklen):
    for i in range(0, len(def_list),def_chunklen):
        yield def_list[i:i + def_chunklen]


##### Parsing the data and writing to the database.
for row in list(DivideList(downstream,10)):
    logger.info('Processing the Downstream Data')
    print('Processing the Downstream Data')
    if row[0] != 'Channel':
        row.append(pulltime)
        ds_i_sql = """INSERT INTO Downstream (Channel,Lock_Status,Modulation,Channel_ID,Frequency,Power,SNR,Unerrored_Codewords,Correctable_Codewords,Uncorrectable_Codewords,Capture_DT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        cur.execute(ds_i_sql,row)
        conn.commit()


for row in list(DivideList(upstream,6)):
    logger.info('Processing the Upstream Data')
    print('Processing the Upstream Data')
    if row[0] != 'Channel':
        row.append(pulltime)
        us_i_sql = """INSERT INTO Upstream (Channel,Lock_Status,Modulation,Channel_ID,Frequency,Power,Capture_DT) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(us_i_sql,row)
        conn.commit()
        
        
for row in list(DivideList(downstreamOFDMA,11)):
    logger.info('Processing the Secondary Downstream Data')
    print('Processing the Secondary Downstream Data')
    if row[0] != 'Channel':
        row.append(pulltime)
        ds_OFDMA_isql = """INSERT INTO Downstream_OFDMA (Channel,Lock_Status,Modulation,Channel_ID,Frequency,Power,SNR,Active_Subcarrier_Number_Range,Unerrored_Codewords,Correctable_Codewords,Uncorrectable_Codewords,Capture_DT) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(ds_OFDMA_isql,row)
        conn.commit()
                
        
for row in list(DivideList(upstreamOFDMA,6)):
    logger.info('Processing the Secondary Upstream Data')
    print('Processing the Secondary Upstream Data')
    if row[0] != 'Channel':
        row.append(pulltime)
        us_OFDMA_isql = """INSERT INTO Upstream_OFDMA (Channel,Lock_Status,Modulation,Channel_ID,Frequency,Power, Capture_DT) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(us_OFDMA_isql,row)
        conn.commit()


##### Closing things up
logger.info('Script Done')
print('Script End')

        