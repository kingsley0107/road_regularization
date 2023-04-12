# %%
import pandas as pd
import geopandas as gpd
from shapely import wkt
import matplotlib.pyplot as plt


def merge_arcpy_raw(arcpy_data_path, raw_data_path):
    # read the data
    arcpy_data = gpd.read_file(arcpy_data_path)[['localId', 'geometry']]
    arcpy_data['localId'] = arcpy_data['localId'].astype('int64')
    raw_data = gpd.read_file(raw_data_path).drop_duplicates(
        subset=['localId'], keep='first')
    # drop the rows with geom_type != LineString from raw
    raw_data = raw_data[raw_data['geometry'].geom_type == 'LineString']
    # drop the rows with localId is null
    arcpy_data = arcpy_data.dropna(subset=['localId'])

    # drop the rows with locald == 0
    arcpy_data = arcpy_data[arcpy_data['localId'] != 0]

    # select the data with duplicated localId
    duplicated = arcpy_data[arcpy_data.duplicated(
        subset=['localId'], keep=False)].sort_values(by=['localId'])

    # delete the duplicated rows from arcpy_data
    arcpy_data_unique = arcpy_data.drop_duplicates(
        subset=['localId'], keep=False)

    # select the data with localId in duplicated from raw_data
    replaced_dups = raw_data[raw_data['localId'].isin(duplicated['localId'])]

    # merge arcpy_data_unique and raw_data on localId
    merged = gpd.GeoDataFrame(arcpy_data_unique.merge(raw_data, on='localId', how='left', suffixes=('_arcpy', '_raw')).rename(
        columns={'geometry_arcpy': 'geometry'}).drop(['geometry_raw'], axis=1), geometry='geometry')

    # concat the merged and replaced_dups
    final = pd.concat([merged, replaced_dups], ignore_index=True)
    return final


# %%
arcpy_res_path = r'C:\Users\20191\Desktop\github\road_regularization\data\arcpy_data\arcpy_res.shp'
raw_data_path = r'C:\Users\20191\Desktop\github\road_regularization\data/测试路网数据/westminster_project.shp'
output_path = r'C:\Users\20191\Desktop\github\road_regularization/data/clean/merged_data2.shp'

merge_arcpy_raw(arcpy_res_path, raw_data_path).to_file(output_path)

# %%
