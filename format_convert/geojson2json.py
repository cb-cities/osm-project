# https://stackoverflow.com/questions/23166158/make-python-script-to-run-forever-on-amazon-ec2
# screen -S <screen_name>
# screen -r <screen_name>
# detached control + A D
# screen -X -S [session # you want to kill] kill
# nohup python3 -u geojson2json.py > out.log 2>&1 &

# nodes1.json			id:       , point:
# links1.json			id:		  , negaid:	  		, posiid:			, polyline: 
# linkgroups.json		group:	  , members:		, toid:				
# roads.geojson		geometry.coordinates:
import re
import os
import json
import geojson

#result file
f_linkgroup = open('linkgroups.json', 'w')
f_link = open('links1.json', 'w')
f_node = open('nodes1.json', 'w')

# point_set is used to store point to avoid duplicate
point_set = []
link_set = 0
# parse coordinates into links.json
def link_write(coordinates):
	global link_set
	f_link.write("{\n")
	#write negativeNode
	NegativeNodeToid = "osgb"+str(4000000000000000+point_set.index(coordinates[0])+1)
	f_link.write("\"negativeNode\": \""+NegativeNodeToid+"\",\n")
	#write toid of link
	toid_link = "osgb"+str(4100000000000000+link_set+1)
	toid_linkgroup = "osgb"+str(4200000000000000+link_set+1)
	f_link.write("\"toid\": \""+toid_link+"\",\n")
	#write linkgroups
	f_linkgroup.write("{\"group\":\"Named Road\",\"members\":[\""+toid_link+"\"],\"toid\":\""+toid_linkgroup+"\"}\n,")
	#write polyline
	f_link.write("\"polyline\": [\n")
	for point in coordinates:
		f_link.write(str(point[0])+',\n'+str(point[1])+',\n')
	f_link.write("],\n")
	#write positiveNode
	PositiveNodeToid = "osgb"+str(4000000000000000+point_set.index(coordinates[-1])+1)
	f_link.write("\"positiveNode\": \""+PositiveNodeToid+"\"\n")
	f_link.write("},\n")
	link_set+=1 

# parse coordinates into node.json
def node_write(coordinates):
	for point in coordinates:	
		if point not in point_set:
			if point_set != []:
				f_node.write(",")
			point_set.append(point)
			if int(len(point_set)/1000)*1000==len(point_set):
				print("Successfully parse "+str(len(point_set))+" points")
			toid = "osgb"+str(4000000000000000+point_set.index(point)+1)
			f_node.write("{\"toid\":\""+toid+"\",\"point\": ["+str(point[0])+','+str(point[1])+"],\"index\":"+str(point_set.index(point)+1)+"}\n")

#there are some non-json data error in geojson file
def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json line: %s" % error)
        return False

# main code 'san-francisco_california_roads.geojson' is filepath
with open(os.path.expanduser('san-francisco_california_roads.geojson'), encoding='utf-8') as fp:
	# two possible json line, one without "," is the end line
	# only extract road car_permission = allowed
	# the set is highway == { motorway or motorway_link or motorway_junction or trunk or trunk_link or primary_link or primary or secondary or tertiary or unclassified or unsurfaced or track or residential or living_street or 
	pattern1 = "^{ \"type\":.*\"type\": \"(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice})\".*},$"
	pattern2 = "^{ \"type\":.*\"type\": \"(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice})\".*}$"
	f_link.write("[\n")
	f_linkgroup.write("[")
	f_node.write("[")
	for line in fp:
		if re.search(pattern1,line):
			if json_validator(line[0:-2]):
				feature = geojson.loads(line[0:-2])		# remove "," and "\n"
				coordinates = feature['geometry']['coordinates']
				node_write(coordinates)
				link_write(coordinates)
		elif re.search(pattern2,line):
			if json_validator(line[0:-1]):
				feature = geojson.loads(line[0:-1])		# remove "\n"
				coordinates = feature['geometry']['coordinates']
				node_write(coordinates)
				link_write(coordinates)
	f_node.write("]")
	f_link.write("]")
	f_linkgroup.write("]")
f_linkgroup.close()
f_link.close()
f_node.close()
print("Successfully parse all geojson roads into links and nodes")
