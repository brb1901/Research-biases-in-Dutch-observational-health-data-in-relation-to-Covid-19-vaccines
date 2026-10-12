import pandas as pd
import gc
# import argparse


def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    versionstr = "_v0"

    filename_core = "GBAPERSOON_trackable_2018_compact_diag_multyears_myoperiendo" + versionstr
    # filename_core = "GBAPERSOON_trackable_2018_compact_diag_multyears_myocardinfarct" + versionstr
    
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")

    filename_core = "GBAPERSOON_trackable_2018and2021_covidinf" + versionstr
    df_c = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_c.shape)

    df_c = df_c[df_c['RINPERSOON'].isin(df_p['RINPERSOON'])] # gevaccineerden gevonden in trackable GBA dataset
    print("After removing RIN-PERSONEN not found in trackable GBA dataset:")
    print(df_c.shape)

    print("\nmerging df_p with df_c\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_c, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    df_p.reset_index(inplace=True,drop=True)
    print(df_p.head())
    print(df_p.shape)

    print("cleaning memory of df_c..")
    df_c.iloc[0:0]
    del df_c
    gc.collect()

    filename_core = "GBAPERSOON_trackable_2018_compact_diag_multyears_covidinf_myoperiendo" + versionstr
    # filename_core = "GBAPERSOON_trackable_2018_compact_diag_multyears_covidinf_myocardinfarct" + versionstr

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    # start = time.time()
    df_p.head(1000).to_csv(filename_csv)
    # print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    # start = time.time()
    df_p.to_feather(filename_ftr)
    # print(time.time() - start)


if __name__ == '__main__':
    run_main()
    


 