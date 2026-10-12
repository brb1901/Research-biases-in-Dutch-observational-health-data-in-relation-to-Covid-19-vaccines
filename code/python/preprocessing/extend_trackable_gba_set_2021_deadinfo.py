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

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    print("reading GBAOVERLIJDEN2023_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2023_ext2.ftr")
    df_o = df_o[ (df_o["jaar_overlijden"] >= refyear) ] # alle doden in dat jaar

    filename_core = "DOODOORZ2020-2023" 
    print("reading " + filename_core + " feather data")
    df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

    print("\nmerging with df_o\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_o[["RINPERSOON","jaar_overlijden","datetimeobj_overlijden"]], how='left', on=["RINPERSOON"])
    # print(time.time() - start)
    print(df_p.head())
    print(df_p.shape)

    print("cleaning memory of df_o..")
    df_o.iloc[0:0]
    del df_o
    gc.collect()


    df_p["dead_bit"] = 0
    df_p["dead_date"] = None
    df_p["dead_cause"] = ""
    df_p["dead_place"] = -1

    print("processing...")

    start_overall = time.time()
    start = time.time()
    nr_dead = 0
    for index, rowdata in df_p.iterrows():
        if index % 100000 == 0:
            print(index)
            # print(rowdata)      
            print(time.time() - start)
            start = time.time()
            print()
        
        # DOOD
        jaar_overlijden = rowdata["jaar_overlijden"]
        if not math.isnan(jaar_overlijden):
            rinp_str = rowdata["RINPERSOON"]
        # rows = df_o.loc[ (df_o["RINPERSOON"] == rinp_str) ]
        # # dead_yq = -1
        # if len(rows): # dus deze persoon is dood
            dead_date = rowdata["datetimeobj_overlijden"]
            # dead = True
            dead_bit = 1
            rows = df_do.loc[ (df_do["RINPERSOON"] == rinp_str) ]
            if len(rows):
                dead_cause = rows.iloc[0]["UCCODE"]
                plovl = rows.iloc[0]["PLOVL"]         
            else:
                dead_cause = "*UNKNOWN*" 
                plovl = -1
            dead_place = int(plovl) 

            df_p.at[index, "dead_bit"] = dead_bit
            df_p.at[index, "dead_date"] = dead_date
            df_p.at[index, "dead_cause"] = dead_cause
            df_p.at[index, "dead_place"] = dead_place
            nr_dead += 1
        
        # if index>10001:
        #     break

    use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER",
                "DEELSCOREWELVAART","DEELSCOREOPLEIDINGSNIVEAU_1","DEELSCORERECENTARBEIDSVERLEDEN","TOTAALSCORE_1",
                "WLZLEVERINGSVORM", "WLZGZZP",
                "WLZ_bit","WLZ_type","WLZ_level","nr_Med_prevyear","med_rxrisk_score_simplesum_prevyear","med_rxrisk_score_weightedpratt_prevyear",
                "dead_bit", "dead_date", "dead_cause", "dead_place"]
    df_p = df_p[use_cols]

    print(df_p.shape)
    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    df_p.reset_index(inplace=True,drop=True)

    print()
    print("Number of dead")
    print(nr_dead)   
    print("Overall processing time:")
    print(time.time() - start_overall)
    print()

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


    