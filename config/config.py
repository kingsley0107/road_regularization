import arcpy


######################################基础配置区,若不修改选中的osm_fclass / qq_subtype ，修改此处路径即可。#################################
# 指定gdb文件夹路径
FILE_ROOT = r'C:/Users/20191/Desktop/数城未来/路网优化/测试过程数据库/'
# 指定新建gdb名称
DATABASE_NAME = 'ROAD_OPTIMIZE.gdb'
# 指定目标城市基础数据路径,文件夹内数据命名格式如下
# 路网数据: 1.osm_xiangcheng.shp 2. qq_xiangcheng.shp
# 边界数据: xiangcheng.shp
ROAD_DATA = r'C:/Users/20191/Desktop/数城未来/路网优化/测试路网数据/'
BOUNDARY_DATA = r'C:/Users/20191/Desktop/数城未来/路网优化/测试边界数据/'
OUTPUT_PATH = r'C:/Users/20191/Desktop/数城未来/路网优化/测试输出数据'
######################################配置区结束#################################


# 最最最主要的道路类别

# TPYES FOR MIXED MODE
OSM_MAIN_FCLASS = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary']
QQ_MAIN_SUBTYPE = ['131184', '131491', '131489']

# TYPES FOR DIVIDED MODE
OSM_MAIN_FCLASS_NO_HIGH = ['primary', 'secondary', 'tertiary']
OSM_MAIN_FCLASS_HIGH = ['motorway', 'trunk']
QQ_MAIN_SUBTYPE_NO_HIGH = ['131184', '131491', '131489']
QQ_MAIN_SUBTYPE_HIGH = ['131332']
# 最终数据中需要保留的字段
fields_to_keep = ["OBJECTID","adcode", "sub_type", "source",
                      "osm_id", "code", "fclass", "name", "type", 'oneway',"SHAPE_Length", "SHAPE"]
# 
MERGING_MAP = {
    'primary':1,
    'secondary':2,
    'tertiary':3,
    'trunk':4,
    'motorway':5
}

Project_ref = arcpy.SpatialReference(3857)
Geographic_ref = arcpy.SpatialReference(4326)


