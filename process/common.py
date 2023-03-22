import arcpy
from config.config import *

def Add_filed(data,field_name,field_type,expression,expression_type):
    arcpy.AddField_management(data, field_name, field_type)
    arcpy.CalculateField_management(data, field_name, expression, expression_type)


def gen_merge_expression(fclass):
    fclass = eval(fclass)
    if fclass.strip().lower() == 'primary':
        return MERGING_MAP['primary']
    elif fclass.strip().lower() == 'secondary':
        return MERGING_MAP['secondary']
    elif fclass.strip().lower() == 'tertiary':
        return MERGING_MAP['tertiary']
    elif fclass.strip().lower() == 'trunk':
        return MERGING_MAP['trunk']
    elif fclass.strip().lower() == 'motorway':
        return MERGING_MAP['motorway']
    else:
        return 0
    
def deleteGDBFile():
    arcpy.Delete_management(FILE_ROOT+DATABASE_NAME)