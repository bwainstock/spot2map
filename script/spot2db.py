#
#Parse Spot JSON for use in DB based mapping solutions
#
#Uses Spot Personal Tracker API to import JSON.  Converts JSON to dict.  Parses dict 
#for lat/long pairs.  Compares unixtime of each lat/long pair to PostgreSQL database 
#to determine if pair is new.  If new, add to PostgreSQL DB.  
#


import json
import urllib
import psycopg2

spotAPIkey = '0lp0XWumH993GUjq0LgzQnddQLR2NoNFN'
#Uncomment following line to use Spot API instead of file
url = urllib.urlopen('https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/' + spotAPIkey + '/message.json')
#url = open('./spotdata.json')

json_data = json.loads(url.read())

data = json_data['response']['feedMessageResponse']['messages']['message']

#PostgreSQL connected requires cursor; Selects maximum unixtime to determine latest entry
try:
    conn = psycopg2.connect("dbname='pct_spot' user='postgres' password='password' host='localhost'")
except:
    print "I am unable to connect to the database."

cur = conn.cursor()
cur.execute("""SELECT MAX(unixtime) FROM points""")
latest = cur.fetchall()
max = latest[0][0]
i = 0
for messages in data:
	if (messages['unixTime'] > max):
		geometry = "POINT(%s %s)" % (messages['longitude'], messages['latitude'])
		print geometry
		print "***********************"
		try:
			sql = """INSERT INTO points VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s,4326));"""
			params = [messages['longitude'], messages['unixTime'], messages['messageType'], messages['dateTime'],
			  messages['showCustomMsg'], messages['messengerName'], messages['messengerId'],
			  messages['batteryState'], messages['latitude'], messages['hidden'], messages['modelId'],
			  messages['id'], messages['@clientUnixTime'], geometry]
			cur.execute(sql, params)
		except:
			print "Unable to execute"

conn.commit()
