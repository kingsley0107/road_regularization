import arcpy 
from config.config import *
from process.preprocess import *
from process.simplify import *
from process.common import *

def process_body(osm_fclass,qq_subtype,CITY:str,smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    # 创建GDB
    try:
        arcpy.CreateFileGDB_management(FILE_ROOT, DATABASE_NAME)
    except:
        print("gdb already exist")
    arcpy.env.workspace = FILE_ROOT+DATABASE_NAME
    arcpy.env.outputMFlag = "DISABLE_M_VALUE"  # 禁用M值输出
    arcpy.env.overwriteOutput = True
    print(f"config workspace : {FILE_ROOT+DATABASE_NAME}")
    OSM_PATH = ROAD_DATA + f'osm_{CITY}.shp'
    QQ_PATH = ROAD_DATA + f'qq_{CITY}.shp'
    BOUNDARY_PATH = BOUNDARY_DATA + f'{CITY}.shp'
    osm_cliped_path = Clip_road(BOUNDARY_PATH,OSM_PATH,'osm')
    qq_cliped_path = Clip_road(BOUNDARY_PATH,QQ_PATH,'qq')
    select_osm = Select_road(osm_fclass,osm_cliped_path,'osm')
    select_qq = Select_road(qq_subtype,qq_cliped_path,'qq')   
    # convert to : 3857
    singlelines = Convert_single(select_osm,select_qq,smooth_level)
    extendedlines = Extend_road(singlelines,extend_distance)
    err_point = Check_topo(extendedlines)
    master_road = Clean_spike(extendedlines,err_point,spike_keep,CITY=CITY,keep_spike=False)
    master_road = Join_attributes('merge',master_road)
    # conver to : 4326 
    res = Delete_fields(master_road,CITY)
    return res
