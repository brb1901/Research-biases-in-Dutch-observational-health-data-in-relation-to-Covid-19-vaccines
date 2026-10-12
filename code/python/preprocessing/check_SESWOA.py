import pandas as pd
import time
# from datetime import date
import gc


def run_main():
    basepath = "H:/data/"
    basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    basepath_csv_seswoa = basepath+"csv/SESWOA/"

    print("reading KOPPELPERSOONHUISHOUDEN2020 and SESWOA2020..")
    df_koppel = pd.read_feather(basepath_ftr_seswoa+"KOPPELPERSOONHUISHOUDEN2020.ftr")
    df_seswoa = pd.read_feather(basepath_ftr_seswoa+"SESWOA2020.ftr")

    print("\nmerging with SESWOA\n")
    # start = time.time()
    df_koppel = pd.merge(df_koppel, df_seswoa, how='left', on=['RINPERSOONHKW'])
    # print(time.time() - start)
    print(df_koppel.head())
    print(df_koppel.shape)

    filename_core = "KOPPELPERSOONHUISHOUDEN2020_SESWOA2020" 

    filename_csv = basepath_csv_seswoa+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    df_koppel.head(1000).to_csv(filename_csv)


    # use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER",
    #             "DEELSCOREWELVAART","DEELSCOREOPLEIDINGSNIVEAU_1","DEELSCORERECENTARBEIDSVERLEDEN","TOTAALSCORE_1"]
    # df_p = df_p[use_cols]



if __name__ == '__main__':
    run_main()


    