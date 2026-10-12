import pandas as pd
import time
# from datetime import date
import gc
import math

def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    versionstr = "_v0"
    # refyear = 2021

    print("reading GBAPERSOON_trackable_2018 feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_2018.ftr")
    print(df_p.shape)

    yearstr = "2018"
    basepath_wlz = basepath+"python_pandas/WLZ/" 
    filename_core = "gebwlz" + yearstr
    filename_ftr = basepath_wlz + filename_core + ".ftr" 
    df_WLZ = pd.read_feather(filename_ftr)
    df_WLZ["WLZGZZP"] = df_WLZ["WLZGZZP"].str.replace('---','0')
    df_WLZ["WLZGZZP"] = df_WLZ["WLZGZZP"].astype(int)

    basepath_wlz_codes = basepath+"csv/WLZ_interpr/" 
    filename_core = "WLZGZZP_interpr_codes"   
    print("reading " + filename_core + " csv data")
    df_WLZ_codes = pd.read_csv(basepath_wlz_codes + filename_core + ".csv") #, keep_default_na=False
    print("making dict")
    dict_WLZ_codes_type = dict(zip(df_WLZ_codes.WLZGZZP_code,df_WLZ_codes.WLZGZZP_type)) # ,df_WLZ_codes.WLZ_level
    # print(dict_WLZ_codes_type)
    dict_WLZ_codes_level = dict(zip(df_WLZ_codes.WLZGZZP_code,df_WLZ_codes.WLZ_level)) # ,df_WLZ_codes.WLZ_level
    # print(dict_WLZ_codes_level)

    print("\nmerging with df_WLZ\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_WLZ, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    print(df_p.head())
    print(df_p.shape)

    print("cleaning memory of df_WLZ..")
    df_WLZ.iloc[0:0]
    del df_WLZ
    gc.collect()

    use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER",
                "DEELSCOREWELVAART","DEELSCOREOPLEIDINGSNIVEAU_1","DEELSCORERECENTARBEIDSVERLEDEN","TOTAALSCORE_1",
                "WLZLEVERINGSVORM", "WLZGZZP"]
    df_p = df_p[use_cols]
    df_p["WLZ_bit"] = 0
    # df_p["WLZLEVERINGSVORM"] = 0
    # df_p["WLZ_code"] = 0
    df_p["WLZ_type"] = 0
    df_p["WLZ_level"] = 0

    start = time.time()
    for index, rowdata in df_p.iterrows():
        if index % 100000 == 0:
            print(index)
            # print(rowdata)      
            print(time.time() - start)
            start = time.time()
            print()
        # WLZLEVERINGSVORM = int(rowdata["WLZLEVERINGSVORM"])
        WLZGZZP = rowdata["WLZGZZP"]
        if not math.isnan(WLZGZZP): # int(WLZGZZP)
            if int(WLZGZZP)>0:
                wlz_type = dict_WLZ_codes_type[WLZGZZP]
                wlz_level = dict_WLZ_codes_level[WLZGZZP]
                # print(wlz_type)
                # print(wlz_level)
                # print()
                df_p.at[index,"WLZ_bit"]=1
                # df_cp.at[index,"WLZLEVERINGSVORM"]=WLZLEVERINGSVORM
                # df_cp.at[index,"WLZ_code"]=WLZGZZP
                df_p.at[index,"WLZ_type"]=wlz_type
                df_p.at[index,"WLZ_level"]=wlz_level
        
        # if index>10001:
        #     break

    print(df_p.shape)
    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    df_p.reset_index(inplace=True,drop=True)

    print()

    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ" + versionstr

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


    