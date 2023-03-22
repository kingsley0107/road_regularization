import arcpy 
from config.config import *

def Convert_single(osm_path,qq_path,threshold):

    arcpy.Merge_management([osm_path,qq_path],'merge')

    arcpy.Project_management('merge','temp',Project_ref)
    arcpy.Buffer_analysis('temp','temp_buffered',f'{threshold} meters')
    # 注意 dissolve会导致路网属性丢失
    # 后续会sjoin回去
    arcpy.Dissolve_management('temp_buffered','temp_buffered_dissolved')
    print("################Extracting centerline")
    arcpy.PolygonToCenterline_topographic('temp_buffered_dissolved','road_singleLine_proj')
    arcpy.Delete_management(['temp','temp_buffered','temp_buffered_dissolved'])
    print("\n")
    # 返回值是该函数的结果,下一函数的输入,注意修改
    return 'road_singleLine_proj'

def Extend_road(roads,distance):
    # start = time.time()
    # print("###########################Extending road")
    arcpy.FeatureToLine_management(roads,'extend_road')
    # 注意记得转投影坐标
    arcpy.ExtendLine_edit('extend_road',f'{distance} meters','EXTENSION')
    arcpy.Delete_management(roads)
    # print(f"###########################Road extended. Time used:{time.time() - start}")
    return 'extend_road'

def Check_topo(roads):
    # print("###########################Strat checking topology")
    # start = time.time()
    dataset_name = 'topo'
    topology_name = 'topology'
    topo_data_name = 'road_data'
    # work tree : topo\topology
    arcpy.CreateFeatureDataset_management(out_name=dataset_name,spatial_reference=Project_ref)
    arcpy.FeatureClassToFeatureClass_conversion(roads,dataset_name,topo_data_name)
    arcpy.CreateTopology_management(dataset_name,topology_name)
    arcpy.AddFeatureClassToTopology_management(f"{dataset_name}/{topology_name}",f"{dataset_name}/{topo_data_name}")
    # print("adding topo rules...")
    # validate 断头点
    arcpy.AddRuleToTopology_management(f"{dataset_name}/{topology_name}","Must Not Have Dangles (Line)",f"{dataset_name}/{topo_data_name}")
    try:
        arcpy.ValidateTopology_management(
            "{0}/{1}".format(dataset_name, topology_name))
    except:
        print('错误数量过大，但是并不影响进程，拓朴验证已修复路网')

    # 输出Topo监测出的断头点
    arcpy.ExportTopologyErrors_management("{0}/{1}".format(dataset_name, topology_name),
                                          out_basename='err')
    arcpy.Delete_management('err_line')
    arcpy.Delete_management('err_poly')
    # print(f"###########################Topology checked. Time used:{time.time()-start}")
    return "err_point"

def  Clean_spike(roads,pts,threshold,CITY,keep_spike = False):
    # start = time.time()
    # print("###########################Clean spike roads")
    arcpy.MakeFeatureLayer_management(roads, 'roads_copy')
    arcpy.SelectLayerByLocation_management('roads_copy',
                                           'INTERSECT',
                                           pts)
    arcpy.CopyFeatures_management('roads_copy',
                                  "spike_roads")
    # 丸姐的断头路需求 这个参数一般不用因此藏起来了，需要的时候可以手动改此处。
    if keep_spike: 
        arcpy.FeatureClassToFeatureClass_conversion(pts,OUTPUT_PATH,f"err_points_{CITY}.shp")
        arcpy.FeatureClassToFeatureClass_conversion("spike_roads",OUTPUT_PATH,f"err_lines_{CITY}.shp")
    spike = "spike_roads"
    if arcpy.Describe("spike_roads").spatialReference.factoryCode != 3857:
        arcpy.Project_management("spike_roads","spike_roads2",Project_ref)
        spike = "spike_roads2"
    # LENGTH_GEODESIC 带有z值的距离
    arcpy.AddGeometryAttributes_management(spike,
                                           'LENGTH_GEODESIC', 'METERS')
    expression = f"LENGTH_GEO < {threshold}"
    arcpy.FeatureClassToFeatureClass_conversion(spike,out_name='to_be_cut',where_clause=expression)
    arcpy.Erase_analysis(roads,'to_be_cut','road_master')
    arcpy.Delete_management('to_be_cut')
    arcpy.Delete_management('spike_roads')
    arcpy.Delete_management('tbc_buffer')
    arcpy.Delete_management('err_point')
    # print(f"###########################Spike roads cleaned. Time used:{time.time()-start}")
    return 'road_master'

def Join_attributes(origin,master):
    # start = time.time()
    # print('###########################Start interrupted_and_spatial_join ...')
    arcpy.Project_management(origin,"origin_proj",Project_ref)
    arcpy.FeatureVerticesToPoints_management(
        master, 'road_master_ends', 'BOTH_ENDS')
    # 1.buffer端点,稍微buffer多一点,可以尽可能避免后面的buffer进行spatialjoin时会接触多个polyline
    arcpy.Buffer_analysis("road_master_ends",'master_pts_buffer','38 meters')
    # 2. 输入带有attribute的raw_road,并且根据步骤1擦除,用于spatial join已经简化后的路网
    arcpy.Erase_analysis("origin_proj",'master_pts_buffer','origin_erasered')
    # 3. 将已经简化后的路网进行buffer 准备spatial join 步骤2 得到的处理后的带有attribute的路网
    arcpy.Buffer_analysis("road_master",'road_master_buffered',"30 meters")
    # 执行featuretoLine，避免一条很长很长的道路因为某一小块蹭到缓冲区，使得缓冲区的属性赋错
    # 经过featuretoLine以及后续匹配规则“MAX”,基本排除spatialJoin误差产生
    arcpy.FeatureToLine_management("origin_erasered","origin_erasered2")
    arcpy.Delete_management("origin_erasered")
    arcpy.Rename_management("origin_erasered2","origin_erasered")
    # 4. 为步骤2的路网添加length,length作为当步骤3的buffer接触多个polyline时,spatialjoin选定的规则应该为length较大的值
    arcpy.AddGeometryAttributes_management("origin_erasered",'LENGTH_GEODESIC','METERS')

        # 创建 FieldMappings 对象
    field_mappings = arcpy.FieldMappings()

    # 添加要素类到 FieldMappings 对象中
    field_mappings.addTable("origin_erasered")
    field_mappings.addTable("road_master_buffered")

    # 获取 FieldMap 对象
    field_map = field_mappings.getFieldMap(
        field_mappings.findFieldMapIndex("LENGTH_GEO"))

    # 将 MergeRule 设置为 Max
    field_map.mergeRule = "Max"

    # 将更新后的 FieldMap 对象替换原有的 FieldMap 对象
    field_mappings.replaceFieldMap(
        field_mappings.findFieldMapIndex("LENGTH_GEO"), field_map)

    # 执行空间连接
    arcpy.SpatialJoin_analysis("road_master_buffered", "origin_erasered",
                                "road_master_buffered_with_attr",
                                field_mapping=field_mappings, join_operation="JOIN_ONE_TO_ONE")
    arcpy.Erase_analysis("road_master","master_pts_buffer",'road_master_erasered')
    arcpy.SpatialJoin_analysis("road_master_erasered","road_master_buffered_with_attr","road_master_with_attr_cliped","JOIN_ONE_TO_ONE",match_option="WITHIN")
    arcpy.SpatialJoin_analysis("road_master","road_master_with_attr_cliped","road_master_new","JOIN_ONE_TO_ONE")
    # print(f"###########################Attribute joined. Time used:{time.time()-start} ")
    arcpy.Delete_management(["master_pts_buffer",'origin_erasered','origin_proj','road_master','road_master_buffered','road_master_buffered_with_attr','road_master_ends','road_master_erasered','road_master_with_attr_cliped'])
    return "road_master_new"

def Delete_fields(roads,CITY):
    # print("###########################Delete Fields")
    # start = time.time()
    all_fields = [f.name for f in arcpy.ListFields(roads)]
    fields_to_delete = [
        f for f in all_fields if f not in fields_to_keep]
    arcpy.DeleteField_management(roads, fields_to_delete)
    arcpy.CopyFeatures_management(roads, "result")
    arcpy.Delete_management(roads)
    flag = "result"
    if arcpy.Describe("result").spatialReference.factoryCode != 3857:
        arcpy.Project_management("result","result2",Project_ref)
        arcpy.Delete_management("result")
        flag = "result2"
    arcpy.AddGeometryAttributes_management(flag,"LENGTH_GEODESIC","METERS")
    arcpy.Project_management(flag,f"road_result_{CITY}",Geographic_ref)
    arcpy.Delete_management(flag)
    arcpy.Delete_management(['topo','extend_road','merge','osm_selected','qq_selected'])
    arcpy.FeatureClassToFeatureClass_conversion(f"road_result_{CITY}",OUTPUT_PATH,f'road_result_{CITY}.shp')
    # print(f"###########################Field deleted. Time used:{time.time()-start}")
    
    return f"road_result_{CITY}"
