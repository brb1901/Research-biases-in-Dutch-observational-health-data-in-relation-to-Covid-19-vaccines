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
    refyear = 2021

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    df_p.drop_duplicates(subset=["RINPERSOON"], inplace=True)
    df_p.reset_index(inplace=True,drop=True)

    print(df_p.shape)

    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    # 

    # print()
    # print("Number of dead")
    # print(nr_dead)   
    # print("Overall processing time:")
    # print(time.time() - start_overall)
    print()

    # versionstr = "_v0B"
    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead" + versionstr

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


    