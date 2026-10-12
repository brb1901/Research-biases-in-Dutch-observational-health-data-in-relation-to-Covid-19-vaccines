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
    # filename_core =  "selectedpeople_with_urban_region_info_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_core =  "selectedpeople_withHKW_SESWOA_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)
    print("reading " + filename_ftr)
    df_uniquepeople = pd.read_feather(filename_ftr)
    print(df_uniquepeople.shape)

    df_uniquepeople["RINP_int"] = df_uniquepeople["RINPERSOON"].astype(int)
    print("Sorting..")
    # df_uniquepeople.sort_values(by=["RINPERSOON"], inplace=True) # , "year", "yearweeknr"
    df_uniquepeople.sort_values(by=["RINP_int"], inplace=True) # , "year", "yearweeknr"
    df_uniquepeople.reset_index(inplace=True,drop=True)
    print()

    
    # filename_core =  "selectedpeople_sorted_with_urban_region_info_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_core =  "selectedpeople_sorted_withHKW_SESWOA_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print("writing: "+filename_ftr)
    # start = time.time()
    df_uniquepeople.to_feather(filename_ftr)
    # print(time.time() - start)
    filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + "_head.csv"
    print("writing: "+filename_csv)
    df_uniquepeople.head(1000).to_csv(filename_csv)
    
if __name__ == '__main__':
    run_main()
    