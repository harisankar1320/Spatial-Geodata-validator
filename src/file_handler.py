import json
import geopandas as gpd

def read_geojson(file):
    if file.name.endswith('.geojson') or file.name.endswith('.json'):
        gdf = gpd.read_file(file)
        return gdf
    else:
        #print("The uploaded file is not valid. Try with GeoJSON or JSON")
        return None
    
