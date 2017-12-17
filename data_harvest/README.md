# Hanxiao Deng's CE299 Project
### Data_Harvest
###### This is code repo for harvesting OpenStreetMap data from Mapzen API to AWS S3 buckets. 
1. San Francisco Mapzen API link:
    - Datasets split by geometry type: lines, points, or polygons (OSM2PGSQL)
        - https://s3.amazonaws.com/metro-extracts.mapzen.com/san-francisco_california.osm2pgsql-geojson.zip
	- Datasets grouped into individual layers by OpenStreetMap tags (IMPOSM)
		- https://s3.amazonaws.com/metro-extracts.mapzen.com/san-francisco_california.imposm-geojson.zip
2. London Mapzen API link:
    - Datasets split by geometry type: lines, points, or polygons (OSM2PGSQL)
		- https://s3.amazonaws.com/metro-extracts.mapzen.com/london_england.osm2pgsql-geojson.zip
	- Datasets grouped into individual layers by OpenStreetMap tags (IMPOSM)
		- https://s3.amazonaws.com/metro-extracts.mapzen.com/london_england.imposm-geojson.zip	
3. New York City Mapzen API link:
	- Datasets split by geometry type: lines, points, or polygons (OSM2PGSQL)
        - https://s3.amazonaws.com/metro-extracts.mapzen.com/new-york_new-york.osm2pgsql-geojson.zip		
	- Datasets grouped into individual layers by OpenStreetMap tags (IMPOSM)
        - https://s3.amazonaws.com/metro-extracts.mapzen.com/new-york_new-york.imposm-geojson.zip