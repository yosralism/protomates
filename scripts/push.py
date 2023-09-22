from influxdb import DataFrameClient
from time import sleep
import json
from os import path
import subprocess
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

while True:
	try:
		client = DataFrameClient(host = 'localhost', port = 8086)
		client.switch_database('home')
		break
	except:
		continue


def main():
	filename = '/home/protomates2/catkin_ws/src/protomates/scripts/out.json'
	listObj = []

	# Check if file exists
	if path.isfile(filename) is False:
		raise Exception("File not found")

	while True:
		while True:
			try:
				results = client.query('SELECT * FROM protomates2 ORDER BY time LIMIT 10')
				df = results['protomates2']
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

		latest_time = 0
		for row in range(df.shape[0]):
			latest_time = round(df.index[row].to_pydatetime().timestamp()*1000000000)
			body = {
				"ts": int(latest_time),
				"values":{
					"latitude": float(df['latitude'][row]),
					"longitude": float(df['longitude'][row]),
					"slope": float(df['slope'][row]),
					"heading": int(df['heading'][row]),
					"fix_type" : str(df['fix_type'][row]),
					"satellites_count": int(df['satellites_count'][row]),
				}
			}
			listObj.append(body)

		# Verify updated list
		print(listObj)
		
		with open(filename, 'w') as json_file:
			json.dump(listObj, json_file, indent=4, separators=(',',': '))

		try:
			# filename = '/home/stac/Projects/PAMA stuff/out.json'
			# check json not empty
			with open(filename) as fp:
				listObj = json.load(fp)
				listObj.pop(0)
			# send json data
			p = subprocess.Popen(['bash','/home/protomates2/catkin_ws/src/protomates/scripts/log.sh'])

			output, err = p.communicate()
			if p.returncode != 0:
				raise Exception("can't connect to thingsboard")

			# clear json file
			open(filename, 'w').close()

			client.query('DELETE FROM protomates2 WHERE time <=' + str(latest_time))

		except:
			logger.info("can't connect to thingsboard, continue to cache data")
			break
			
		sleep(2)

main()
