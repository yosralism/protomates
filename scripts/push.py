#!/usr/bin/env python

from influxdb import DataFrameClient
from time import sleep
import json
from os import path
import subprocess
import logging
import mysql.connector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mysql_host = "100.114.108.141"
mysql_user = "smartd_admin"
mysql_password = "Pama123!@#"
mysql_db = "PRG_DB"

while True:
    try:
        client = DataFrameClient(host = 'localhost', port = 8086)
        client.switch_database('home')
        break
    except:
        continue


def main():
    filename = '/home/pamaprg/catkin_ws/src/protomates/scripts/out.json'
    listObj = []

    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")

    while True:
        try:
            mysql_conn = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_password,database=mysql_db)
            cursor = mysql_conn.cursor()
        except:
            pass
        while True:
            try:
                results = client.query('SELECT * FROM smartd ORDER BY time LIMIT 100')
                df = results['smartd']
                break
            except:
                continue
        # Read JSON file
        try:
            with open(filename) as fp:
                listObj = json.load(fp)
        except:
            listObj = []

        # Verify existing list
        print(listObj)

        print(type(listObj))
        listData = []
        latest_time = 0
        for row in range(df.shape[0]):
            latest_time = round(df.index[row].to_pydatetime().timestamp()*1000000000)
            try:
                body = {
                        "ts": int(latest_time),
                        "values":{
                                "latitude": float(df['latitude'][row]),
                                "longitude": float(df['longitude'][row]),
                                "altitude": float(df['altitude'][row]),
                                "slope": float(df['slope'][row]),
                                "heading": int(df['heading'][row]),
                                "fix_type" : str(df['fix_type'][row]),
                                "satellites_count": int(df['satellites_count'][row]),
                        }
                }
                listObj.append(body)
                data_insert = (int(latest_time), float(df['latitude'][row]), float(df['longitude'][row]), float(df['altitude'][row]), float(df['slope'][row]),  int(df['heading'][row]), str(df['fix_type'][row]), int(df['satellites_count'][row]))
                listData.append(data_insert)
            except:
                continue
        try:
            insert_query = "INSERT INTO prg_data (ts, latitude, longitude, altitude, slope, heading, gps_type, satellites_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s )"
            cursor.executemany(insert_query, listData)
            mysql_conn.commit()
            print(body)
            cursor.close()
            mysql_conn.close()
            # Verify updated list
            print(listObj)

            with open(filename, 'w') as json_file:
                json.dump(listObj, json_file, indent=4, separators=(',',': '))
        except:
            pass
        try:
            # filename = '/home/stac/Projects/PAMA stuff/out.json'
            # check json not empty
            with open(filename) as fp:
                listObj = json.load(fp)
                listObj.pop(0)
            # send json data
            p = subprocess.Popen(['bash','/home/pamaprg/catkin_ws/src/protomates/scripts/log.sh'])

            output, err = p.communicate()
            if p.returncode != 0:
                raise Exception("can't connect to thingsboard")

            # clear json file
            open(filename, 'w').close()

            client.query('DELETE FROM smartd WHERE time <=' + str(latest_time))

        except:
            logger.info("can't connect to thingsboard, continue to cache data")
            break

        sleep(2)

main()
