import pandas as pd
import numpy as np
import os
import geopandas as gpd
from pyproj import CRS, Transformer


class prepare_GTFS():

    # Read in the GTFS data
    def __init__(self) -> None:
        self.file_path = r'C:\Users\zma\Documents\GitHub\BQI_MATSIM'
        self.time_table_path = os.path.join(self.file_path, 'Timetable_IBX.xlsx')
        self.output_path = os.path.join(self.file_path, 'output')
    
    def read_time_table(self, sheet_name):
        df = pd.read_excel(self.time_table_path, sheet_name=sheet_name)
        return df

    def prepare_route(self):
        # write txt file with route information
        # The columns are: route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color
        # Hard code the route information as a dictionary
        route_dict = {"route_id": "IBX",
                      "agency_id": "MTA NYCT",
                        "route_short_name": "IBX",
                        "route_long_name": "Interborough Express",
                        "route_desc": "The Interborough Express is a transformative rapid transit project that will connect currently underserved areas of Brooklyn and Queens",
                        "route_type": 3,
                        "route_url": "https://new.mta.info/project/interborough-express",
                        "route_color": "00FFFF",
                        "route_text_color": "000000"}
        
        # Write the route information into a txt file
        # Convert the dictionary into a dataframe
        route_df = pd.DataFrame.from_dict(route_dict, orient='index').T
        route_df.to_csv(os.path.join(self.output_path, 'routes.txt'), index=False)

    def prepare_shape(self):
        # write txt file with shape information
        # The columns are: shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
        # shape_dist_traveled is optional, usually left blank

        # Read the shapefile
        gdf = gpd.read_file(os.path.join(self.file_path, 'GIS/Unofficial BQI Route.shp'))
        print(gdf)
        # Iterate through each feature and extract the coordinates
        line_coords = []
        for line in gdf['geometry']:
            if line.geom_type == 'LineString':
                coords = list(line.coords)
                line_coords.append(coords)

        # Replace this with the correct EPSG code for your source coordinate system
        source_crs = CRS("EPSG:26918")
        target_crs = CRS("EPSG:4326")  # WGS 84 - the standard geographic coordinate system
        transformer = Transformer.from_crs(source_crs, target_crs)
        lon_lat_coords = [transformer.transform(x, y) for x, y in line_coords[0]]



        # Create a dataframe with the shape information
        shape_df = pd.DataFrame(lon_lat_coords, columns=['shape_pt_lon', 'shape_pt_lat'])
        shape_df['shape_id']='Interborough_Express'
        shape_df['shape_dist_traveled']=np.nan
        shape_df['shape_pt_sequence']=shape_df.index
        shape_df = shape_df[['shape_id','shape_pt_lat','shape_pt_lon','shape_pt_sequence','shape_dist_traveled']]

        # Write the shape information into a txt file
        shape_df.to_csv(os.path.join(self.output_path, 'shapes.txt'), index=False)




if __name__ == '__main__':
    gtfs = prepare_GTFS()
    #df = gtfs.read_time_table('bk_bound')
    #gtfs.prepare_route()
    gtfs.prepare_shape()
