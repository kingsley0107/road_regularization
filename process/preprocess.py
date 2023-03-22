import arcpy
import time
from process.common import *
from config.config import *

def Clip_road(boundary, road, source):

    if arcpy.Exists(road):
        print(f'{road} exist')
        arcpy.Clip_analysis(road, boundary,f'{source}_cliped')
        if source == 'osm':
            fields = ['name','ref']
            cursor = arcpy.UpdateCursor(road)
            for row in cursor:
                if row.getValue(fields[0]) == " ":
                    row.setValue(fields[0],row.getValue(fields[1]))
                    cursor.updateRow(row)
        return f"{source}_cliped"
    else:
        raise ValueError(f"DATA {road} NOT EXIST!!!!")


def Select_road(keep_list,road_path,source):
    if len(keep_list)> 1:
        expression = f"fclass in {tuple(keep_list)}" if source=='osm' else f"sub_type in {tuple(keep_list)}"
    else :
        expression = f"fclass in ('{keep_list[0]}')" if source=='osm' else f"sub_type in ('{keep_list[0]}')"
    if arcpy.Exists(road_path):
        arcpy.FeatureClassToFeatureClass_conversion(road_path,out_name=f'{source}_selected',where_clause=expression)
    else:
        raise ValueError(f"DATA {road_path} NOT EXIST!!!!")
    arcpy.Delete_management(f"{road_path}")
    return f'{source}_selected'
