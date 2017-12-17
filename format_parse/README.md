# Hanxiao Deng's CE299 Project
### Data Format Parse
This is code repo for parsing OpenStreetMap data from geojson file to json file in [sierra-charlie](https://github.com/hxdengBerkeley/sierra-charlie). 
### Usage
make sure you have right file in the folder.
```
screen -S parse
nohup python3 -u geojson2json_geometry.py > out.log 2>&1 &
Crtl + A + D to detach screen
```
### File needed in folder
- geojson2json_geometry
	- san-francisco_california_osm_point.geojson
	- san-francisco_california_osm_line.geojson
- geojson2json_geometry
 	- san-francisco_california_roads.geojson
 	- san-francisco_california_roads_gen0.geojson
 	- san-francisco_california_roads_gen1.geojson
 	- san-francisco_california_transport_points.geojson