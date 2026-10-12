import os
import pandas as pd
import time
import gc
# import argparse

def run_main():
    basepath = "H:/data/"
    basepath_ftr_vektis = basepath+"python_pandas/VEKTIS/"
    basepath_csv_vektis = basepath + "csv/VEKTIS/"
    # basepath_csv_regios = basepath + "csv/postcodes_regios_mateverstedelijking/"

    versionstr = "_v0"
    # max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    firstyear = 2018
    lastyear = 2021
    sel_string = "zac_33238_3323[12345]"
    # yearstr = str(firstyear)

    # filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_core =  "selectedpeople_with_urban_region_info_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)
    print("reading " + filename_ftr)
    df_uniquepeople = pd.read_feather(filename_ftr)
    print(df_uniquepeople.shape)

    min_rinp_int = 1
    max_rinp_int = min_rinp_int-1 + 1000000

    rinp_str = "-1"
    rinp_int_prev = int(rinp_str)
    rinp_str_prev = rinp_str
    rinp_str_prev_prev = rinp_str_prev
    list_RINP = []
    list_RINP_prev = []
    list_RINP_prev_prev = []
    list_min_rinp = []
    list_max_rinp = []
    nr_weird = 0
    for index, rowdata in df_uniquepeople.iterrows():
        if index % 1000 == 0:
            print(index)
            print()

        rinp_str = int(rowdata["RINPERSOON"])  
        rinp_int = int(rinp_str)
        if rinp_int<rinp_int_prev:
            list_RINP.append(rinp_str)
            list_RINP_prev.append(rinp_str_prev)
            list_RINP_prev_prev.append(rinp_str_prev_prev)
            list_min_rinp.append(min_rinp_int)
            list_max_rinp.append(max_rinp_int)
            nr_weird += 1
            print(rinp_str)
            print(rinp_str_prev)
            print(rinp_str_prev_prev)
            print(min_rinp_int)
            print(max_rinp_int)
            print()
        elif rinp_int>max_rinp_int:
            min_rinp_int = max_rinp_int+1
            max_rinp_int = min_rinp_int-1 + 1000000

        rinp_str_prev_prev = rinp_str_prev
        rinp_int_prev = rinp_int
        rinp_str_prev = rinp_str

    print("nr_weird: " + str(nr_weird) )
    df_out = pd.DataFrame()
    df_out["list_RINP"] = list_RINP
    df_out["list_RINP_prev"] = list_RINP_prev
    df_out["list_RINP_prev_prev"] = list_RINP_prev_prev
    df_out["list_min_rinp"] = list_min_rinp
    df_out["list_max_rinp"] = list_max_rinp

    print(df_out.head())

    # use_cols = ['RINPERSOON','RINPERSOONHKW','DEELSCOREWELVAART','DEELSCOREOPLEIDINGSNIVEAU_1','DEELSCORERECENTARBEIDSVERLEDEN','TOTAALSCORE_1']
    # df_uniquepeople = df_uniquepeople[use_cols]

    filename_core =  "selectedpeople_WEIRD_with_urban_region_info_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print("writing: "+filename_ftr)
    # start = time.time()
    df_out.to_feather(filename_ftr)
    # print(time.time() - start)
    filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + ".csv"
    print("writing: "+filename_csv)
    df_out.to_csv(filename_csv)
    
if __name__ == '__main__':
    run_main()
    