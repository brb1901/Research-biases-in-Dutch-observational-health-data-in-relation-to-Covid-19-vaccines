import pandas as pd
import gc
# import argparse


def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    # versionstr = "_v0"

    print("reading GBAPERSOON_trackable_2018 feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_2018.ftr")
    print(df_p.shape)

    print("selecting only some columns for compact dataset..")
    use_cols = ["RINPERSOON"]
    df_p = df_p[use_cols]

    print("reading GBAPERSOON_trackable_2021 feather data")
    df_p2 = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_2021.ftr")
    print(df_p2.shape)

    print("selecting only some columns for compact dataset..")
    use_cols = ["RINPERSOON"]
    df_p2 = df_p2[use_cols]

    df_p = pd.concat([df_p,df_p2], ignore_index=True) 
    df_p = df_p.drop_duplicates(subset = "RINPERSOON")
    df_p.reset_index(inplace=True,drop=True)
    
    filename_core = "GBAPERSOON_trackable_2018and2021"
    # filename_core = "GBAPERSOON_trackable_2018_compact_diag_multyears_myocardinfarct" + versionstr

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
    


 