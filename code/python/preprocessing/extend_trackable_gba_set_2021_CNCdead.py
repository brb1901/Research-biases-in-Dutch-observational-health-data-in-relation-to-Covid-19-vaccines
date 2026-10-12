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

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")

    df_p["dead_bit_covid"] = 0
    df_p["dead_bit_noncovid"] = 0

    print("Covid deaths:")
    m = ( (df_p["dead_bit"]==1) & (df_p["dead_cause"].str.startswith("U07")) )
    df_p.loc[m, "dead_bit_covid"] = 1
    df_sel = df_p[(df_p["dead_bit"]==1) & (df_p["dead_cause"].str.startswith("U07"))]
    print(len(df_sel))

    print("Non-Covid deaths:")
    m = ( (df_p["dead_bit"]==1) & (df_p["dead_cause"].str.startswith("U07")==False) )
    df_p.loc[m, "dead_bit_noncovid"] = 1
    df_sel = df_p[(df_p["dead_bit"]==1) & (df_p["dead_cause"].str.startswith("U07")==False)]
    print(len(df_sel))

    print()

    # versionstr = "_v0B"
    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead" + versionstr

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



if __name__ == '__main__':
    run_main()


    