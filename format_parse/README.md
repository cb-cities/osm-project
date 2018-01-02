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
### Notes
- There are two different source OpenStreetMap data to be converted into JSON data for Sierra-Charlie. [Mapzen File Format](https://mapzen.com/documentation/metro-extracts/file-format/). 
eg. for London [Download Links](https://mapzen.com/data/metro-extracts/metro/london_england/)
    1. Datasets split by geometry type: lines, points, or polygons. Files following:
        - london_england_osm_line.geojson
        - london_england_osm_point.geojson
        - london_england_osm_polygon.geojson
    2. Datasets grouped into individual layers by OpenStreetMap tags.
        - london_england_roads_gen0.geojson
        - london_england_roads_gen1.geojson
        - london_england_roads.geojson
- There are two defferent python code to parse data from the two source.
    1. By geometry
        - geojson2json_geometry.py
        - You need: 
            1. london_england_osm_line.geojson
            2. london_england_osm_point.geojson
    2. By tags
        - geojson2json_tags.py
        - You need:
            1. san-francisco_california_roads.geojson
            2. san-francisco_california_roads_gen0.geojson
            3. san-francisco_california_roads_gen1.geojson
