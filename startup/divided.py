import arcpy 
from config.config import *
from process.preprocess import *
from process.simplify import *
from process.common import *
from startup.schedule import process_body
def start_process_divided(road_type:str,osm_fclass,qq_subtype,CITY:str,smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    if road_type not in ['highway', 'no_highway']:
        raise ValueError("Invalid road_type. Must be 'highway' or 'no_highway'.")
    res = process_body(osm_fclass,qq_subtype,CITY,smooth_level= smooth_level, extend_distance=extend_distance, spike_keep = spike_keep)
    arcpy.FeatureClassToFeatureClass_conversion(res,OUTPUT_PATH,f'road_result_{CITY}_{road_type}.shp')
    return f"{OUTPUT_PATH}/road_result_{CITY}_{road_type}.shp"

def divided_start(i,smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    res1 = start_process_divided('no_highway',OSM_MAIN_FCLASS_NO_HIGH,QQ_MAIN_SUBTYPE_NO_HIGH,i,smooth_level = smooth_level,extend_distance=extend_distance,spike_keep=spike_keep)
    arcpy.Delete_management(f"{OUTPUT_PATH}/road_result_{i}.shp")
    res2 = start_process_divided('highway',OSM_MAIN_FCLASS_HIGH,QQ_MAIN_SUBTYPE_HIGH,i,smooth_level = smooth_level,extend_distance=extend_distance,spike_keep=spike_keep)
    arcpy.Delete_management(f"{OUTPUT_PATH}/road_result_{i}.shp")
    arcpy.Merge_management([res1,res2],f"{OUTPUT_PATH}/road_result_{i}_merge.shp")
    arcpy.FeatureToLine_management(f"{OUTPUT_PATH}/road_result_{i}_merge.shp",f"{OUTPUT_PATH}/road_result_{i}_merged.shp")
    arcpy.Delete_management([res1,res2,f"{OUTPUT_PATH}/road_result_{i}_merge.shp"])
    arcpy.DeleteField_management(f"{OUTPUT_PATH}/road_result_{i}_merged.shp",['LENGTH_GEO'])
    deleteGDBFile()
    return f"{OUTPUT_PATH}/road_result_{i}_merged.shp"