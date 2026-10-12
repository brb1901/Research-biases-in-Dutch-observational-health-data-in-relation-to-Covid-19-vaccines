import pandas as pd
import time
# from datetime import date
import gc
import math
import os

def run_main():
    basepath = "H:/data/"
    basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    basepath_ftr_medicijn = basepath+"python_pandas/MEDICIJN/"

    versionstr = "_v0"
    # refyear = 2021

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    df_p["RINP_int"] = df_p["RINPERSOON"].astype(int)
    # print("*** DEBUG SKIPPING Sorting..")
    print("Sorting..")
    # df_uniquepeople.sort_values(by=["RINPERSOON"], inplace=True) # , "year", "yearweeknr"
    df_p.sort_values(by=["RINP_int"], inplace=True) # , "year", "yearweeknr"
    df_p.reset_index(inplace=True,drop=True)
    print()

    # use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER",
    #             "DEELSCOREWELVAART","DEELSCOREOPLEIDINGSNIVEAU_1","DEELSCORERECENTARBEIDSVERLEDEN","TOTAALSCORE_1",
    #             "WLZLEVERINGSVORM", "WLZGZZP"]
    # df_p = df_p[use_cols]

    # take data from one year BEFORE refyear 2021
    yearstr = "2020"

    df_p["nr_Med_prevyear"] = 0
    df_p["med_rxrisk_score_simplesum_prevyear"] = 0
    df_p["med_rxrisk_score_weightedpratt_prevyear"] = 0

    max_rinp_int = 0
    min_rinp_int = 1
    start = time.time()
    for index, rowdata in df_p.iterrows():
        if index % 100000 == 0:
            print(index)
            # print(rowdata)      
            print(time.time() - start)
            start = time.time()
            print()

        rinp_str = rowdata["RINPERSOON"]
        rinp_int = rowdata["RINP_int"]
        # print(rinp_str)
        if rinp_int>max_rinp_int:
            min_rinp_int = max_rinp_int+1
            max_rinp_int = min_rinp_int-1 + 1000000
            filename_core =  "MEDICIJNPerY_" + yearstr + "_atc_rxrisk_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
            filename_ftr = basepath_ftr_medicijn + "atc_rxrisk/" + filename_core + ".ftr" 
            file_exists = os.path.exists(filename_ftr)
            # print(rinp_int)
            # print(min_rinp_int)
            # print(max_rinp_int)
            # print()
            print(filename_ftr)
            if file_exists:
                df_med_prevyear = pd.read_feather(filename_ftr)
        
        rows_p_prev = df_med_prevyear.loc[df_med_prevyear["RINPERSOON"]==rinp_str]
        if len(rows_p_prev):
            nr_Med = int(rows_p_prev.iloc[0]["nr_Med"])
            score_simplesum = int(rows_p_prev.iloc[0]["score_simplesum"])
            score_weightedpratt = int(rows_p_prev.iloc[0]["score_weightedpratt"])
            df_p.at[index,"nr_Med_prevyear"]=nr_Med
            df_p.at[index,"med_rxrisk_score_simplesum_prevyear"]=score_simplesum
            df_p.at[index,"med_rxrisk_score_weightedpratt_prevyear"]=score_weightedpratt
        
        # if index>10001:
        #     break

    print(df_p.shape)
    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    df_p.reset_index(inplace=True,drop=True)

    print()

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed" + versionstr

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


    