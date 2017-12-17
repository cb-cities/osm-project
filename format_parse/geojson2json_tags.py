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
#f_linkgroup = open('linkgroups.json', 'w')
f_link = open('links1.json', 'w')
f_node = open('nodes1.json', 'w')

# point_set is used to store point to avoid duplicate
point_dict = {}
link_set = 0
no_node = 0

# parse coordinates into links.json
def link_write(coordinates,properties):
	global link_set, no_node
	NegativeNode = coordinates[0]
	PositiveNode = coordinates[-1]
	if (NegativeNode[0],NegativeNode[1]) in point_dict and (PositiveNode[0],PositiveNode[1]) in point_dict:
		f_link.write("{\n")
		#write "index": 0,
		f_link.write("\"index\": "+str(link_set)+",\n")
		#write "term": "A Road",
		f_link.write("\"term\": \""+"Motorway"+"\",\n")
		#write "restriction": "One Way",
		f_link.write("\"restriction\": \""+"One Way"+"\",\n")
		#write "nature": "Roundabout",
		f_link.write("\"nature\": \""+"Dual Carriageway"+"\",\n")
		#write negativeNode
		NegativeNodeToid = point_dict[(NegativeNode[0],NegativeNode[1])]
		f_link.write("\"negativeNode\": \""+NegativeNodeToid+"\",\n")
		#write toid of link
		#toid_link = "osgb"+str(4100000000000000+link_set)
		toid_link = "osgb"+str(4000000000000000+round(properties['osm_id']))
		#toid_linkgroup = "osgb"+str(4200000000000000+link_set+1)
		f_link.write("\"toid\": \""+toid_link+"\",\n")
		#write linkgroups
		##f_linkgroup.write("{\"group\":\"Named Road\",\"members\":[\""+toid_link+"\"],\"toid\":\""+toid_linkgroup+"\"}\n,")
		#write polyline
		f_link.write("\"polyline\": [\n")
		for point in coordinates:
			if point == coordinates[-1]:
				f_link.write(str(point[0])+',\n'+str(point[1])+'\n')
			else:
				f_link.write(str(point[0])+',\n'+str(point[1])+',\n')
		f_link.write("],\n")
		#write positiveNode
		PositiveNodeToid = point_dict[(PositiveNode[0],PositiveNode[1])]
		f_link.write("\"positiveNode\": \""+PositiveNodeToid+"\",\n")
		#write "orientation": "+"
		f_link.write("\"orientation\": \""+"-"+"\"\n")
		f_link.write("},\n")
		link_set+=1
		if 1000*round(link_set/1000)==link_set:
			print("links - Successfully parse "+str(link_set)+" links")
	else:
		no_node+=1
		if round(no_node/100)*100 == no_node:
			print(no_node)

# parse coordinates into node.json
def node_write(coordinates):
	point = coordinates
	if not (point[0],point[1]) in point_dict:
		if point_dict:
			f_node.write(",")
		if int(len(point_dict)/1000)*1000==len(point_dict):
			print("points - Successfully parse "+str(len(point_dict))+" points")
		toid = "osgb"+str(4000000001000000+round(len(point_dict))+1)
		point_dict[(point[0],point[1])] = toid
		f_node.write("{\"toid\":\""+toid+"\",\"point\": ["+str(point[0])+','+str(point[1])+"],\"index\":"+str(len(point_dict))+"}\n")

# line to node write
def line_write_node(line):
	pattern1 = "coordinates(.*),$"
	pattern2 = "coordinates(.*)$"
	if re.search(pattern1,line):
		if json_validator(line[0:-2]):
			feature = geojson.loads(line[0:-2])		# remove "," and "\n"
			coordinates = feature['geometry']['coordinates']
			osm_id = feature['properties']['osm_id']
			coordinates = [round(coordinates[0]*1000),round(coordinates[1]*1000)]
			node_write(coordinates,osm_id)
	elif re.search(pattern2,line):
		if json_validator(line[0:-1]):
			feature = geojson.loads(line[0:-1])		# remove "\n"
			coordinates = feature['geometry']['coordinates']
			osm_id = feature['properties']['osm_id']
			coordinates = [round(coordinates[0]*1000),round(coordinates[1]*1000)]
			node_write(coordinates,osm_id)

# line to link write
def line_write_link(line):
	# two possible json line, one without "," is the end line
	# only extract road car_permission = allowed
	# the set is highway == { motorway 1515 or motorway_link 3007 or motorway_junction 0 or trunk 1024 or trunk_link 108 or primary_link 256 or primary 5352 or secondary 9207 or tertiary 6865 or unclassified 1371 or unsurfaced 0 or track 1402 or residential 33780 or living_street 68.
	pattern1 = "{ .*\"highway\": \"(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice)\".*},"
	pattern2 = "{ .*\"highway\": \"(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice)\".*}"
	for line in fp:
		if re.search(pattern1,line):
			if json_validator(line[0:-2]):
				feature = geojson.loads(line[0:-2])		# remove "," and "\n"
				coordinates = feature['geometry']['coordinates']
				coordinates = [[round(point[0]*1000),round(point[1]*1000)] for point in coordinates]
				properties = feature['properties']
				link_write(coordinates,properties)
		elif re.search(pattern2,line):
			if json_validator(line[0:-1]):
				feature = geojson.loads(line[0:-1])		# remove "\n"
				coordinates = feature['geometry']['coordinates']
				coordinates = [[round(point[0]*1000),round(point[1]*1000)] for point in coordinates]
				properties = feature['properties']
				link_write(coordinates,properties)

# line to link write
def line_write_node_and_link(line):
	# two possible json line, one without "," is the end line
	# only extract road car_permission = allowed
	# the set is highway == { motorway 1515 or motorway_link 3007 or motorway_junction 0 or trunk 1024 or trunk_link 108 or primary_link 256 or primary 5352 or secondary 9207 or tertiary 6865 or unclassified 1371 or unsurfaced 0 or track 1402 or residential 33780 or living_street 68.
	pattern1 = "{ .*\"highway\": \"(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice)\".*},"
	pattern2 = "{ .*\"highway\": \"(motorway|motorway_link|motorway_junction|trunk|trunk_link|primary_link|primary|secondary|tertiary|unclassified|unsurfaced|track|residential|living_street|dservice)\".*}"
	for line in fp:
		feature = {}
		if re.search(pattern1,line):
			if json_validator(line[0:-2]):
				feature = geojson.loads(line[0:-2])		# remove "," and "\n"
		elif re.search(pattern2,line):
			if json_validator(line[0:-1]):
				feature = geojson.loads(line[0:-1])		# remove "\n"
		if feature:
			coordinates = feature['geometry']['coordinates']
			coordinates = [[round(point[0]*100000),round(point[1]*100000)] for point in coordinates]
			properties = feature['properties']
			if not coordinates[0]==coordinates[-1]:
				node_write(coordinates[0])
				node_write(coordinates[-1])
				link_write(coordinates,properties)

#there are some non-json data error in geojson file
def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        print("invalid json line: %s" % error)
        return False

# main code 'san-francisco_california_osm_line.geojson' is filepath
# write nodes1.json links1.json
with open(os.path.expanduser('san-francisco_california_osm_line.geojson'), encoding='utf-8') as fp:
	f_node.write("[")
	f_link.write("[\n")
	while True:
		try:
			line = fp.readline()
			if not line:
				break
			else:
				line_write_node_and_link(line)
		except UnicodeDecodeError as error:
			print("invalid json line: %s" % error)
	f_node.write("]")
	f_link.write("]")
	#f_linkgroup.write("]")
f_node.close()
f_link.close()
print("Successfully parse all nodes and links")