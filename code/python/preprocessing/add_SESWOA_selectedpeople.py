import os
import pandas as pd
import time
import gc
# import argparse

def run_main():
    basepath = "H:/data/"
    basepath_ftr_vektis = basepath+"python_pandas/VEKTIS/"
    basepath_csv_vektis = basepath + "csv/VEKTIS/"
    basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"

    versionstr = "_v0"
    # max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    firstyear = 2018
    lastyear = 2021
    sel_string = "zac_33238_3323[12345]"

    filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)

    print("reading " + filename_ftr)
    df_in = pd.read_feather(filename_ftr)
    print(df_in.shape)

    print("reading GBAPERSOON_trackable_years2018-2022_ext feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_years2018-2022_ext.ftr")

    df_uniquepeople = df_in.drop_duplicates(subset = "RINPERSOON")
    print(df_uniquepeople.shape)
    print(df_uniquepeople.head())

    print("dropping non-trackable..")
    df_uniquepeople = df_uniquepeople[  (df_uniquepeople['RINPERSOON'].isin(df_p['RINPERSOON']))  ]
    print(df_uniquepeople.shape)
    print(df_uniquepeople.head())
    # df_p_unique = df_p[  (df_p['RINPERSOON'].isin(df_uniquepeople['RINPERSOON']))  ]

    print("cleaning memory..")
    df_p.iloc[0:0]
    del df_p
    gc.collect()

    print("reading KOPPELPERSOONHUISHOUDEN2018 and SESWOA2018..")
    df_koppel = pd.read_feather(basepath_ftr_seswoa+"KOPPELPERSOONHUISHOUDEN2018.ftr")
    df_seswoa = pd.read_feather(basepath_ftr_seswoa+"SESWOA2018.ftr")

    print("\nmerging with KOPPELPERSOONHUISHOUDEN\n")
    # start = time.time()
    df_uniquepeople = pd.merge(df_uniquepeople, df_koppel, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    print(df_uniquepeople.head())
    print(df_uniquepeople.shape)

    print("\nmerging with SESWOA\n")
    # start = time.time()
    df_uniquepeople = pd.merge(df_uniquepeople, df_seswoa, how='left', on=['RINPERSOONHKW'])
    # print(time.time() - start)
    print(df_uniquepeople.head())
    print(df_uniquepeople.shape)

    use_cols = ['RINPERSOON','RINPERSOONHKW','DEELSCOREWELVAART','DEELSCOREOPLEIDINGSNIVEAU_1','DEELSCORERECENTARBEIDSVERLEDEN','TOTAALSCORE_1']
    df_uniquepeople = df_uniquepeople[use_cols]

    filename_core =  "selectedpeople_withHKW_SESWOA_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
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
    