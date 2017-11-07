# node.json			id:       , point:
# link.json			negaid:	  , posiid:			, polyline: 
# roads.geojson		geometry.coordinates:
import re
import os
import json
import geojson

#result file
f_link = open('links.json', 'w')
f_node = open('nodes.json', 'w')

# point_set is used to store point to avoid duplicate
point_set = []

# parse coordinates into links.json
def link_write(coordinates):
	f_link.write("{\n")
	#write negativeNode
	NegativeNodeToid = "osgb"+str(4000000000000000+point_set.index(coordinates[0])+1)
	f_link.write("\"negativeNode\": \""+NegativeNodeToid+"\",\n")
	#write polyline
	f_link.write("\"polyline\": [\n")
	for point in coordinates:
		f_link.write(str(point[0])+',\n'+str(point[1])+',\n')
	f_link.write("],\n")
	#write positiveNode
	PositiveNodeToid = "osgb"+str(4000000000000000+point_set.index(coordinates[-1])+1)
	f_link.write("\"positiveNode\": \""+PositiveNodeToid+"\"\n")
	f_link.write("},\n")

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
	pattern1 = "^{ \"type\":.*},$"
	pattern2 = "^{ \"type\":.*}$"
	f_link.write("[\n")
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
f_link.close()
f_node.close()
print("Successfully parse all geojson roads into links and nodes")