import pandas as pd
import time
# from datetime import date
import gc
import math
import os

def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    # basepath_ftr_medicijn = basepath+"python_pandas/MEDICIJN/"

    versionstr = "_v0"
    # refyear = 2021

    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ_ComorbMed_Dead" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    print("reading CIMSDATA_20230801_onerowpp feather data")
    df_cims = pd.read_feather(basepath+"python_pandas/CIMS/"+"CIMSDATA_20230801_onerowpp.ftr")
    print(df_cims.shape)

    df_cims = df_cims[df_cims['RINPERSOON'].isin(df_p['RINPERSOON'])] # gevaccineerden gevonden in trackable GBA dataset
    print("After removing RIN-PERSONEN not found in trackable GBA dataset:")
    print(df_cims.shape)

    print("\nmerging df_p with df_cims\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_cims, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    df_p.reset_index(inplace=True,drop=True)
    print(df_p.head())
    print(df_p.shape)

    print("cleaning memory of df_cims..")
    df_cims.iloc[0:0]
    del df_cims
    gc.collect()

    # print(df_p.shape)

    print()

    # versionstr = "_v0B"
    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ_ComorbMed_Dead_Vax" + versionstr

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_p.head(1000).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_p.to_feather(filename_ftr)
    print(time.time() - start)

    # print("Skipping dta (Stata) now!")
    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_p.to_stata(filename_dta)
    # print(time.time() - start)

if __name__ == '__main__':
    run_main()


    