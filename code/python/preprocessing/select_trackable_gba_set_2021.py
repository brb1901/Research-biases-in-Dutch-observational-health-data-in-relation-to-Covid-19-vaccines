import pandas as pd
import time
# from datetime import date
import gc


def run_main():
    basepath = "H:/data/"
    basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    versionstr = "_v0"

    refyear = 2021

    df_fo = df_o[ (df_o["jaar_overlijden"] < refyear)  ] # year &  (df_o['RINPERSOON'].isin(df_p['RINPERSOON']))
    nr_deaths_before_refyear = len(df_fo)
    print("Number of deaths before refyear: " + str(nr_deaths_before_refyear))

    print("reading GBAPERSOON_trackable_years2018-2022_ext feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_years2018-2022_ext.ftr")
    print(df_p.shape)

    df_p = df_p[~df_p['RINPERSOON'].isin(df_fo['RINPERSOON'])]
    print("After removing deaths before refyear: ")
    print(df_p.shape)        
    print()

    print("cleaning memory of df_o and df_fo..")
    df_fo.iloc[0:0]
    del df_fo
    gc.collect()
    df_o.iloc[0:0]
    del df_o
    gc.collect()

    print("reading KOPPELPERSOONHUISHOUDEN2020 and SESWOA2020..")
    df_koppel = pd.read_feather(basepath_ftr_seswoa+"KOPPELPERSOONHUISHOUDEN2020.ftr")
    df_seswoa = pd.read_feather(basepath_ftr_seswoa+"SESWOA2020.ftr")

    print("\nmerging with KOPPELPERSOONHUISHOUDEN\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_koppel, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    print(df_p.head())
    print(df_p.shape)

    print("\nmerging with SESWOA\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_seswoa, how='left', on=['RINPERSOONHKW'])
    # print(time.time() - start)
    print(df_p.head())
    print(df_p.shape)

    print("cleaning memory of df_koppel and df_seswoa..")
    df_koppel.iloc[0:0]
    del df_koppel
    gc.collect()
    df_seswoa.iloc[0:0]
    del df_seswoa
    gc.collect()

    use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER",
                "DEELSCOREWELVAART","DEELSCOREOPLEIDINGSNIVEAU_1","DEELSCORERECENTARBEIDSVERLEDEN","TOTAALSCORE_1"]
    df_p = df_p[use_cols]

    print(df_p.shape)
    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    df_p.reset_index(inplace=True,drop=True)

    print()

    filename_core = "GBAPERSOON_trackable_2021"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_p.head(100).to_csv(filename_csv)
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


    