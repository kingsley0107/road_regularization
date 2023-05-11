English  [中文版](./zh-cn.md)  
# road_geo_regularization
### A universal simplification of the main road network in the city, which can be used for non-high precision land division, etc.

### Performance:
#### raw road data
- ![overview](./img/micro_raw.jpg)
#### simplified road data
- ![overview](./img/micro_processed.jpg)


### Environment:
- Arcgis Pro
- Python 3.x from Arcgis Pro 
- Arcpy from Arcgis Pro
- Encoding utf-8_sig

### Required Data:
- Road network data
- Boundary data
- Data needs to be placed in the path specified in config.py in advance, pay attention to the naming format

### User Manual:
1. Specify directories manually in config/config.py

    - Configuration options:
        -  ./config/config.py needs to be manually specified:
        -   GDB file path (automatically created if it doesn't exist), GDB will be automatically cleared if all steps are executed successfully
        -   Road network data root directory (pay attention to the naming conventions of road network data)
        -   Boundary data root directory (pay attention to the naming conventions)
    -   Road types:
        -   Currently, road types are selected mainly for the purpose of parcel division. The road network categories involved in the simplification are filtered based on the ROAD_TYPE_FIELD in config.py. You can add a new category in config.py for customized fine road network processing.

2.  Execute main.py

    -   The main function start_process in main.py accepts the following parameters:
        -   CITY: City name, ensure the naming is the same as the suffix of the road network (see comments for details)
        -   MODE: Simplification mode, must be 'mixed'
        -   smooth_level: Level of simplification, the higher the value, the smoother the result (distortion)
        -   extend_distance: Distance of extending dead-end roads, the higher the value, the more closed road networks (but may extend a road where it does not exist)
        -   spike_keep: Threshold for cleaning small spikes, roads with a length lower than this threshold will be removed, the higher the value, the more regular the roads, but it may remove roads that are actually dead-ends

### Road Network Simplification Principle:
1.  Extract CenterLines
    - ![load data](./img/process/load.jpg)
        <p align="center">
                <i>load raw data.</i>
        </p>
    - ![buffer road](./img/process/buffer.jpg)
        <p align="center">
            <i>build buffer for each line.</i>
        </p>
    - ![dissolve road](./img/process/dissolve.jpg)
        <p align="center">
            <i>dissolve the buffers.</i>
        </p>
    - ![ extract ](./img/process/extract.jpg)
        <p align="center">
            <i>Extract centerlines from merged buffers</i>
        </p>
    - ![ res ](./img/process/step1res.jpg)
    <p align="center">
        <i>Extraction result.</i>
    </p>
2.  road optimization:
    - ![ res ](./img/process/extend.jpg)
        <p align="center">
            <i>Extension of non-closed roads (in blue).</i>
        </p>
    - ![ res ](./img/process/spikep.jpg)
        <p align="center">
            <i>Extraction of dead-end roads (points).</i>
        </p>    
    - ![ res ](./img/process/threshold.jpg)
            <p align="center">
                <i>Filtering small spikes (in red) with a length below the threshold.</i>
            </p>                 
3.  Road Network Spatial Information Re-association:：
    - ![ res ](./img/process/getinfo.jpg)
    <p align="center">
        <i>Create buffers based on the simplified road network and load the original road network data for information assignment.</i>
    </p>
    
    - ![ res ](./img/process/sjoinprinc.jpg)
    <p align="center">
        <i>For each buffer, the matching rule with the original road network is to select the most representative road within the buffer (largest overlap).</i>
    </p>
    
    - ![ res ](./img/process/sjoinprinc_2.jpg)
        <p align="center">
        <i>eg. The most representative road within this buffer is enclosed.</i>
    </p>
4.  output result
    - ![result](./img/process/res.jpg)

### A Hidden Parameter:
There is a hidden parameter called keep_spike in the clean_spike function in simplify.py, which is not commonly used.

It may be useful when plotting data related to dead-end roads. If needed, you can manually set keep_spike to True.

The data for dead-end points and dead-end lines will be output to the result path, named 'err_points.shp' and 'err_lines.shp', respectively.