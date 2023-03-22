# road_geo_regularization
### Simplification of main road network for cities that do not require high precision for land subdivision, etc.

### Environment:
- Arcgis Pro
- Python 3.x from Arcgis Pro 
- Arcpy from Arcgis Pro
- Encoding utf-8_sig

### Required Data:
- OSM road network data
- QQ road network data
- Administrative boundary data for target city
- Data needs to be placed according to the naming format in config.py beforehand.

### Instructions:
1. Manually specify the directory in config/config.py first
    - Configuration items:
        - ./config/config.py needs to be manually specified:
            - GDB file path (will be automatically created if not exist), GDB will be emptied when all steps are successfully executed.
            - Root directory of road network data (pay attention to the naming rules of road network data)
            - Root directory of boundary data (pay attention to the naming rules)
            - Simplified road output folder (OUTPUT_PATH) (.shp file)

        - Road category:
            - Currently, the choice of road types is mainly for the purpose of land subdivision, and all road networks within the land block are excluded. New types can be added for customized and fine road network processing in the future.
            - When MODE is mixed, high-level bridges and normal roads are not distinguished, and all types are simplified at the same time. Road types are configured in config.py:
                - OSM_MAIN_FCLASS['motorway', 'trunk', 'primary', 'secondary', 'tertiary']
                - QQ_MAIN_SUBTYPE: ['131184', '131491', '131489']
            - When MODE is divided, high-level bridges and normal roads are distinguished. The road networks of OSM and QQ need to be processed for high-level bridges and normal roads separately. Road types are configured in config.py:
                - OSM_MAIN_FCLASS_NO_HIGH：['primary', 'secondary', 'tertiary']
                - OSM_MAIN_FCLASS_HIGH = ['motorway', 'trunk']
                - QQ_MAIN_SUBTYPE_NO_HIGH = ['131184', '131491', '131489']
                - QQ_MAIN_SUBTYPE_HIGH = ['131332']
2. Run main.py.
    - The start_process function of main.py's main parameter:
        - CITY: City name, pay attention to the naming needs to be the same as the road network suffix (see comments for details).
        - MODE: Simplification mode, must be one of 'mixed' or 'divided'.
        - smooth_level: Simplification degree, the higher the value, the smoother the result (distortion).
        - extend_distance: The distance of the broken road extension. The higher the value, the more closed road networks there are (but a road will extend to places without roads).
        - spike_keep: The threshold for cleaning up tiny broken roads. Roads with lengths lower than this threshold will be removed. The higher the value, the more regular the roads will be, but some roads that are actually broken in reality may disappear.

### Overall Processing Method:
1.  preprocess：
    - Road network clipping by boundary
    - select by attribute 
2.  Convert Multiple to Single:
    - Merge qq & osm
    - Buffer & Dissolve
    - Extract Center lines
3.  Road Network Noise Reduction：
    - Topology check (find broken roads, verify connectivity)
    - Remove trivial roads with broken endings
    - Re-sjoin feature attributes based on the approximation degree between centerline and raw_road.

### A Hidden Parameter:
There is a "keep_spike" parameter hidden in the clean_spike function in simplify.py, which is not used very often.

if you want to export the broken end roads, edit the param: keep_spike to True manually.

the broken point will be export as 'err_points.shp' and the lines as 'err_lines.shp'