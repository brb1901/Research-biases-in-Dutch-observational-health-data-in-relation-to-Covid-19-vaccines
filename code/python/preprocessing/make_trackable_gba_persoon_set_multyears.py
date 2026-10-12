import pandas as pd
import time
# from datetime import date


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    # basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    yearfirst = 2016
    yearlast = 2020

    filename_core = "GBAPERSOON" + str(yearfirst-1) + "_presentalivethatwholeyear" # dit zijn mensen die op 1 jan 2018 (yearfirst) er zouden moeten zijn
    print("reading " + filename_core + " feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")

    use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER"]
    df_p = df_p[use_cols]
    print(df_p.shape)
    size = len(df_p["RINPERSOON"])
    print(size)
    # keeplist = [int(1)] * size
    df_p["keeplist"] = 1 # keeplist
    # jaar_overlijden = [int(-1)] * size
    df_p["jaar_overlijden"] = -1 # jaar_overlijden

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    filename_core = "DOODOORZ2015-2022" 
    print("reading " + filename_core + " feather data")
    df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

    print("keeplist at start: ")
    print(df_p["keeplist"].sum())

    df_fo = df_o[ (df_o["jaar_overlijden"] < yearfirst) ] # alle doden VOOR HET EERSTE jaar
    m1 = df_p['RINPERSOON'].isin(df_fo['RINPERSOON'])
    # m2 = df_fo['RINPERSOON'].isin(df_p['RINPERSOON'])
    df_p.loc[m1 ,"keeplist"] = 0
    df_p.loc[m1 ,"jaar_overlijden"] = 1900 #df_fo[m2 ,"jaar_overlijden"]
    print("keeplist after removing dead from before yearfirst: ")
    print(df_p["keeplist"].sum())      
    print()

    for year in [2016, 2017, 2018, 2019, 2020]: # [2018, 2019, 2020, 2021, 2022]
        yearstr = str(year)
        print(yearstr)
        # yearnext = year+1

        df_fo = df_o[ (df_o["jaar_overlijden"] == year) ] # alle doden in dat jaar
        print("Number of people who died this year: " + str(len(df_fo)))

        df_dood_notok = df_fo[~df_fo['RINPERSOON'].isin(df_do['RINPERSOON'])] # dode NIET gevonden in doodoorzaken
        print("Number of people who died this year and Do NOT have cause of death (NOT OK): " + str(len(df_dood_notok)))
        m = df_p['RINPERSOON'].isin(df_dood_notok['RINPERSOON'])
        df_p.loc[m ,"keeplist"] = 0 # df_p.loc[m ,"keeplist"].replace(1,0)

        df_dood_ok = df_fo[df_fo['RINPERSOON'].isin(df_do['RINPERSOON'])] # dode gevonden in doodoorzaken
        print("Number of people who died this year AND have cause of death (OK): " + str(len(df_dood_ok)))
        m = df_p['RINPERSOON'].isin(df_dood_ok['RINPERSOON'])
        df_p.loc[m ,"jaar_overlijden"] = year # df_p.loc[m ,"jaar_overlijden"].replace(-1,year)  #  keep these!
        # df_p.loc[df_p['RINPERSOON'].isin(df_dood_ok['RINPERSOON']) ,"keeplist"] = 1

        df_fp = df_p[df_p["keeplist"]==0]
        print("Number of people removed until now: " + str(len(df_fp)))
        df_fp = df_p[df_p["jaar_overlijden"]==year]
        print("Number of trackable people who died this year and are OK: " + str(len(df_fp)))

        print("keeplist after removing not-ok dead: ")
        print(df_p["keeplist"].sum())

        if year <= yearlast:
            filename_core_next = "GBAPERSOON" + str(year) + "_presentalivethatwholeyear" # dit zijn mensen die op 31 dec (van dit year) er nog zouden moeten zijn
            print("reading " + filename_core_next + " feather data (next)")
            df_p_next = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core_next + ".ftr")
            df_p_next = df_p_next[use_cols]

            # not found in next year GBA_PERSOON, and not found among the dead of this year AND years before:
            # df_fo = df_o[ (df_o["jaar_overlijden"] <= year) ] # alle doden in dat jaar EN JAREN ERVOOR  # & (df_o["jaar_overlijden"] >= 1900)
            # df_p_notdead = df_p[~df_p['RINPERSOON'].isin(df_fo['RINPERSOON'])]
            df_p_notdead_notalrrem = df_p[ (df_p["jaar_overlijden"] == -1) & (df_p["keeplist"]==1) ] # (df_p["jaar_overlijden"] <= year) & (df_p["jaar_overlijden"] >= 1900)
            df_p_notfound = df_p_notdead_notalrrem[~df_p_notdead_notalrrem['RINPERSOON'].isin(df_p_next['RINPERSOON'])  ]
            print("Number of people who did not die in or before this year AND CANNOT be found in GBA_PERSOON end of this year (NOT OK): " + str(len(df_p_notfound)))

            df_p.loc[df_p['RINPERSOON'].isin(df_p_notfound['RINPERSOON']) ,"keeplist"] = 0

            print("keeplist after removing not-found in next year: ")
            print(df_p["keeplist"].sum())


    df_p = df_p[df_p["keeplist"]==1]

    use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND","jaar_overlijden","GBAGEBOORTELAND","GBAGEBOORTELANDMOEDER","GBAGEBOORTELANDVADER"]
    df_p = df_p[use_cols]

    print(df_p.shape)
    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    df_p.reset_index(inplace=True,drop=True)

    print()

    # #DEBUG: TESTING CODE ONLY:
    # use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND"]
    # for year in [2018, 2019, 2020, 2021, 2022]: 
    #     yearstr = str(year)
    #     print(yearstr)
    #     # yearnext = year+1

    #     df_fp = df_p[ (df_p["jaar_overlijden"] == year) ] # alle OK doden in dat jaar, zouden dit moeten zijn
    #     print("Number of people who died this year and are OK: " + str(len(df_fp)))

    #     if year <= yearlast:
    #         filename_core_next = "GBAPERSOON" + str(year) + "_presentalivethatwholeyear" # dit zijn mensen die op 31 dec (van dit year) er nog zouden moeten zijn
    #         print("reading " + filename_core_next + " feather data (next)")
    #         df_p_next = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core_next + ".ftr")
    #         df_p_next = df_p_next[use_cols]

    #         # not found in next year GBA_PERSOON, and not found among the dead of this year AND years before:
    #         # df_fo = df_o[ (df_o["jaar_overlijden"] <= year) ] # alle doden in dat jaar EN JAREN ERVOOR  # & (df_o["jaar_overlijden"] >= 1900)
    #         # df_p_notdead = df_p[~df_p['RINPERSOON'].isin(df_fo['RINPERSOON'])]
    #         df_p_notdead = df_p[ (df_p["jaar_overlijden"] == -1) ] # (df_p["jaar_overlijden"] <= year) & (df_p["jaar_overlijden"] >= 1900)
    #         df_p_notfound = df_p_notdead[~df_p_notdead['RINPERSOON'].isin(df_p_next['RINPERSOON'])  ]
    #         print("Number of people who did not die in or before this year AND CANNOT be found in GBA_PERSOON end of this year (NOT OK): " + str(len(df_p_notfound)))


    filename_core = "GBAPERSOON_trackable_years2016-2020_ext" # "GBAPERSOON_trackable_years2018-2022_ext"

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

    print("Skipping dta (Stata) now!")
    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_p.to_stata(filename_dta)
    # print(time.time() - start)

if __name__ == '__main__':
    run_main()


    