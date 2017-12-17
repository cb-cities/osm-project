#run this by nohup
#nohup python -u harvest.py > out.log 2>&1 &
import sched, time
def data2s3():
	localtime = time.localtime(time.time())
	timelable = str(localtime[0])+'-'+str(localtime[1])+'-'+str(localtime[2])
	fulltimelable = str(localtime[0])+'-'+str(localtime[1])+'-'+str(localtime[2])+' '+str(localtime[3])+':'+str(localtime[4])+':'+str(localtime[5])
	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	#boto3
	#Creating the Connection
	import boto3
	s3 = boto3.resource('s3')
	#download san francisco data
	import urllib2
	print "downloading San Francisco OSM data  time:"+fulltimelable
	url = "https://s3.amazonaws.com/metro-extracts.mapzen.com/san-francisco_california.imposm-geojson.zip"
	f = urllib2.urlopen(url)
	data = f.read()
	with open("./tmp/san-francisco_	california.imposm-geojson.zip", "wb") as code:
	    code.write(data)
	f.close()
	print "successfully downloaded San Francisco OSM data  time:"+fulltimelable
	#Upload san fracisco data
	print "uploading San Francisco OSM data  time:"+fulltimelable
	s3.Object('osm-ucb', timelable+'san-francisco_california.imposm-geojson.zip').put(Body=open('./tmp/san-francisco_california.imposm-geojson.zip', 'rb'))
	print "successfully downloaded San Francisco OSM data  time:"+fulltimelable

	#download New York data
	import urllib2
	print "downloading New York OSM data  time:"+fulltimelable
	url = "https://s3.amazonaws.com/metro-extracts.mapzen.com/new-york_new-york.imposm-geojson.zip"
	f = urllib2.urlopen(url)
	data = f.read()
	with open("./tmp/new-york_new-york.imposm-geojson.zip", "wb") as code:
	    code.write(data)
	f.close()
	print "successfully downloaded New York OSM data  time:"+fulltimelable
	#Upload New York data
	print "uploading New York OSM data  time:"+fulltimelable
	s3.Object('osm-ucb', timelable+'new-york_new-york.imposm-geojson.zip').put(Body=open('./tmp/new-york_new-york.imposm-geojson.zip', 'rb'))
	print "successfully downloaded New York OSM data  time:"+fulltimelable

	#download London data
	import urllib2
	print "downloading London OSM data  time:"+fulltimelable
	url = "https://s3.amazonaws.com/metro-extracts.mapzen.com/london_england.imposm-geojson.zip"
	f = urllib2.urlopen(url)
	data = f.read()
	with open("./tmp/london_england.imposm-geojson.zip", "wb") as code:
	    code.write(data)
	f.close()
	print "successfully downloaded London OSM data  time:"+fulltimelable
	#Upload London data
	print "uploading London OSM data  time:"+fulltimelable
	s3.Object('osm-ucb', timelable+'london_england.imposm-geojson.zip').put(Body=open('./tmp/london_england.imposm-geojson.zip', 'rb'))
	print "successfully downloaded London OSM data  time:"+fulltimelable

#run this timely
def harvest_timely():
	s = sched.scheduler(time.time, time.sleep)	
	while True:
		s.enter(60*60, 1, data2s3, ())
		s.run()

harvest_timely()
