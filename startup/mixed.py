import arcpy 
from config.config import *
from process.preprocess import *
from process.simplify import *
from startup.schedule import process_body
from process.common import *
import time
def start_process_mixed(road_type:str,osm_fclass,CITY:str,smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    if road_type not in ['mixed']:
        raise ValueError("Invalid road_type. Must be 'mixed'.")
    res = process_body(osm_fclass,CITY,smooth_level= smooth_level, extend_distance=extend_distance, spike_keep = spike_keep)
    # arcpy.FeatureClassToFeatureClass_conversion(res,OUTPUT_PATH,f'road_result_{CITY}_{road_type}.shp')
    # arcpy.Delete_management([res])
    return res

def mixed_start(i,smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    res = start_process_mixed('mixed',OSM_MAIN_FCLASS,i,smooth_level,extend_distance,spike_keep)
    # deleteGDBFile()
    return res

