import pandas as pd
import time
# from datetime import date


def look_for_person(rinp, df):
    print("looking for: " + rinp)
    row = df.loc[df["RINPERSOON"]==rinp]
    if row.size:
        print("found: " + rinp)
        print(row.iloc[0]["GBAGEBOORTEJAAR"])
    else:
        print("not found")

def process_data_oneyear(year, basepath_dta, basepath_ftr, basepath_csv, df_o):
    yearstr = str(year)
    print("reading GBAPERSOON_ext" + yearstr + " feather data")
    start = time.time()
    df_p = pd.read_feather(basepath_ftr+"GBAPERSOON" + yearstr + "_ext.ftr")
    print(time.time() - start)
    print(df_p.shape)

    print("selecting deaths before or in " + yearstr)
    df_f = df_o[df_o["jaar_overlijden"] <= year]
    df_f.reset_index(inplace=True,drop=True)
    print(df_f.shape)

    print("\nmaking new filtered df: removing deaths that year or years before")
    start = time.time()
    df_m = df_p[~df_p['RINPERSOON'].isin(df_f['RINPERSOON'])]
    # df_m = pd.merge(df_p, df_o, how='outer', on=['RINPERSOON'], indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)
    df_m.reset_index(inplace=True,drop=True)
    print(time.time() - start)
    print(df_m.shape)
    print()

    df_p  = df_m
    
    print("reading GBASTANDBEVOLKING" + yearstr + " feather data")
    start = time.time()
    df_s = pd.read_feather(basepath_ftr+"GBASTANDBEVOLKING" + yearstr + ".ftr")
    print(time.time() - start)

    print("\nmaking new filtered df: only keeping those still GBA registered at end of year")
    start = time.time()
    df_m = df_p[df_p['RINPERSOON'].isin(df_s['RINPERSOON'])]
    # df_m = pd.merge(df_p, df_o, how='outer', on=['RINPERSOON'], indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)
    df_m.reset_index(inplace=True,drop=True)
    print(time.time() - start)
    print(df_m.shape)
    print()


    filename_core = "GBAPERSOON" + yearstr + "_presentalivethatwholeyear"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_m.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_m.to_feather(filename_ftr)
    print(time.time() - start)

    print("Skipping dta (Stata) now!")
    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_p.to_stata(filename_dta)
    # print(time.time() - start)

    print()


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    print("reading GBAOVERLIJDEN2022_ext feather data")
    start = time.time()
    df_o = pd.read_feather(basepath_ftr+"GBAOVERLIJDEN2022_ext.ftr")
    print(time.time() - start)
    print(df_o.shape)

    for year in [2015, 2016]: # [2017, 2018, 2019, 2020, 2021, 2022] 2015, 2016, 2017, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
        process_data_oneyear(year, basepath_dta, basepath_ftr, basepath_csv, df_o)


if __name__ == '__main__':
    run_main()
    


 