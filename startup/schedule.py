import arcpy 
from config.config import *
from process.preprocess import *
from process.simplify import *
from process.common import *

def process_body(osm_fclass,CITY:str,smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    # 创建GDB
    try:
        arcpy.CreateFileGDB_management(FILE_ROOT, DATABASE_NAME)
    except:
        print("gdb already exist")
    arcpy.env.workspace = FILE_ROOT+DATABASE_NAME
    arcpy.env.outputMFlag = "DISABLE_M_VALUE"  # 禁用M值输出
    arcpy.env.overwriteOutput = True
    print(f"config workspace : {FILE_ROOT+DATABASE_NAME}")
    OSM_PATH = ROAD_DATA + f'{CITY}.shp'
    BOUNDARY_PATH = BOUNDARY_DATA + f'{CITY}.shp'
    # use arcpy to check the factory code:
    if not arcpy.Describe(OSM_PATH).spatialReference.factoryCode == PROJ_CRS:
        arcpy.Project_management(OSM_PATH,ROAD_DATA + f'{CITY}_project.shp',Project_ref)
        OSM_PATH = ROAD_DATA + f'{CITY}_project.shp'
    if not arcpy.Describe(BOUNDARY_PATH).spatialReference.factoryCode == PROJ_CRS:
        arcpy.Project_management(BOUNDARY_PATH,BOUNDARY_DATA + f'{CITY}_project.shp',Project_ref)
        BOUNDARY_PATH = BOUNDARY_DATA + f'{CITY}_project.shp'
    
    osm_cliped_path = Clip_road(BOUNDARY_PATH,OSM_PATH)
    select_osm = Select_road(osm_fclass,osm_cliped_path)
    raw_road = select_osm
    # convert to : 3857
    singlelines = Convert_single(select_osm,smooth_level)
    print(f"Convert_single Finish:{singlelines}")
    extendedlines = Extend_road(singlelines,extend_distance)
    print("Extend roads Finish")
    err_point = Check_topo(extendedlines)
    print("Check Topo Finish")
    master_road = Clean_spike(extendedlines,err_point,spike_keep,CITY=CITY,keep_spike=False)
    print("Clean Spike Finish")
    master_road = Join_attributes(raw_road,master_road)
    # conver to : 4326 
    res = Delete_fields(master_road,CITY)
    return res
