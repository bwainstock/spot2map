'''
#
#Parse Spot JSON for use in DB based mapping solutions
#
#Uses Spot Personal Tracker API to import JSON.  Converts JSON to dict.  Parses dict
#for lat/long pairs.  Compares unixtime of each lat/long pair to PostgreSQL database
#to determine if pair is new.  If new, add to PostgreSQL DB
#
'''

import json
import sys
import urllib
import psycopg2


def main():
    '''
    Everything
    '''

    spot_api_key = '0lp0XWumH993GUjq0LgzQnddQLR2NoNFN'
    #Uncomment following line to use Spot API instead of file
    url = 'https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/'
    #resp = urllib.urlopen(url + spot_api_key + '/message.json')
    resp = open('./spotdata.json')

    json_data = json.loads(resp.read())

    data = json_data['response']['feedMessageResponse']['messages']['message']

    #PostgreSQL connected requires cursor; Selects maximum unixtime to determine latest entry
    try:
        database = 'pct_spot'
        user = 'postgres'
        password = 'password'
        host = 'localhost'
        conn = psycopg2.connect(database=database, user=user, password=password, host=host)
    except psycopg2.OperationalError:
        print "WARNING: Unable to connect to the database."
        sys.exit(1)

    cur = conn.cursor()
    cur.execute("""SELECT MAX(unixtime) FROM points""")
    latest = cur.fetchall()
    max_timestamp = latest[0][0]
    for messages in data:
        if messages['unixTime'] > max_timestamp:
            geometry = "POINT(%s %s)" % (messages['longitude'], messages['latitude'])
            print geometry
            print "***********************"
            try:
                sql = """
                    INSERT INTO points
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    ST_GeomFromText(%s,4326));
                    """
                params = [messages['longitude'],
                          messages['unixTime'],
                          messages['messageType'],
                          messages['dateTime'],
                          messages['showCustomMsg'],
                          messages['messengerName'],
                          messages['messengerId'],
                          messages['batteryState'],
                          messages['latitude'],
                          messages['hidden'],
                          messages['modelId'],
                          messages['id'],
                          messages['@clientUnixTime'],
                          geometry]
                cur.execute(sql, params)
            except psycopg2.Error:
                print "Unable to execute"

    conn.commit()


if __name__ == '__main__':
    main()
