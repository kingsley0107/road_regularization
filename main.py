# -*- coding: utf-8 -*-
from startup.divided import *
from startup.mixed import *



def start_process(CITY:str,mode:str = 'divided',smooth_level:int = 30,extend_distance:int = 100,spike_keep:int = 500):
    """_summary_

    Args:
        CITY (str): city to be processed, which is the key for finding the corresponding road data. eg. CITY: 'xiangcheng' -> OSM_PATH:'osm_xiangcheng.shp' 
        mode : 'divided': split highway and non-highway when process the data while 'mixed' means mix them and process in one time.
        smooth_level (int, optional): The higher the smoother. The value that controls the level of simplification and smoothing of the road, the essence is the distance of the buffer that will be extracted centerlines. Defaults to 30.
        extend_distance (int, optional): extend_level . Defaults to 100.
        spike_keep (int, optional): Threshold to keep the spike. Defaults to 500.
    """    
    if mode not in ['divided','mixed']:
        raise ValueError("😅Invalid mode. Must be 'divided' or 'mixed'.😅")
    if mode == 'divided':
        print("🙁 type divided is underfixing 🙁")
        res = divided_start(CITY,smooth_level = smooth_level,extend_distance=extend_distance,spike_keep=spike_keep)
    elif mode == 'mixed':
        res = mixed_start(CITY,smooth_level = smooth_level,extend_distance=extend_distance,spike_keep=spike_keep)

    return res


if __name__ == '__main__':
    # MODE: 'mixed' | 'divided'
    MODE ='mixed'
    for i in ['westminster']:
        print(f"😈😈😈😈😈            Begin process {i}                     😈😈😈😈😈")
        print(f"😈😈😈😈😈            MODE: {MODE}                                😈😈😈😈😈")
        start_time = time.time()
        output_path = start_process(i,MODE,smooth_level = 10,extend_distance=100,spike_keep=50)
        # output_path = start_process(i,'mixed',smooth_level = 30,extend_distance=100,spike_keep=500)
        print(f"🤭🤭🤭🤭🤭            {i} processed                             🤭🤭🤭🤭🤭")
        print(f"🎉🎉🎉🎉🎉            time used: {time.time()- start_time}  🎉🎉🎉🎉🎉")
        print(f"🚀🚀🚀🚀🚀            CITY {i} MODE {MODE} result: {output_path}   🚀🚀🚀🚀🚀")