# import os
import pandas as pd
# import time
# import gc
# import argparse
import matplotlib.pyplot as plt

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
    # selectedpeople_sorted_withHKW_SESWOA_2018_2021_zac_33238_3323[12345]_v0_head
    filename_core =  "selectedpeople_sorted_withHKW_SESWOA_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)
    print("reading " + filename_ftr)
    df_uniquepeople = pd.read_feather(filename_ftr)
    # print(df_uniquepeople.shape)

    min_rinp_int = 1
    max_rinp_int = min_rinp_int-1 + 1000000

    df_uniquepeople.hist(column=["DEELSCOREWELVAART"], bins = 30, grid = False)
    plt.show()
    df_uniquepeople.hist(column=["DEELSCOREOPLEIDINGSNIVEAU_1"], bins = 30, grid = False)
    plt.show()
    df_uniquepeople.hist(column=["DEELSCORERECENTARBEIDSVERLEDEN"], bins = 30, grid = False)
    plt.show()
    df_uniquepeople.hist(column=["TOTAALSCORE_1"], bins = 30, grid = False)
    plt.show()
    
if __name__ == '__main__':
    run_main()
    