import os
import pandas as pd
import time
import gc
# import argparse

def run_main():
    basepath = "H:/data/"
    basepath_ftr_vektis = basepath+"python_pandas/VEKTIS/"
    basepath_csv_vektis = basepath + "csv/VEKTIS/"
    basepath_csv_regios = basepath + "csv/postcodes_regios_mateverstedelijking/"

    versionstr = "_v0"
    # max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    firstyear = 2018
    lastyear = 2021
    sel_string = "zac_33238_3323[12345]"
    yearstr = str(firstyear)

    filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)
    print("reading " + filename_ftr)
    df_uniquepeople = pd.read_feather(filename_ftr)
    print(df_uniquepeople.shape)

    filename_core = "postcode_MateVanStedelijkheidEtc_v1"   
    print("reading " + filename_core + " csv data")
    df_sted = pd.read_csv(basepath_csv_regios + filename_core + ".csv", encoding="ISO-8859-1") #, keep_default_na=False

    filename_core = "postcodes_regios_simpel_v2"   
    print("reading " + filename_core + " csv data")
    df_regios = pd.read_csv(basepath_csv_regios + filename_core + ".csv", encoding="ISO-8859-1") #, keep_default_na=False

    print("reading GBASTANDBEVOLKING" + yearstr + " feather data")
    df_s = pd.read_feather(basepath+"python_pandas/GBA/"+"GBASTANDBEVOLKING" + yearstr + ".ftr")

    print("making dict for mate van stedelijkheid")
    dict_sted = {}
    for index, rowdata in df_sted.iterrows():
        if index % 10000 == 0:
            print(index)
        if len(rowdata["MeestVoorkomendePostcode_114"]) and rowdata["MeestVoorkomendePostcode_114"]!="  ":
            postcode = int(rowdata["MeestVoorkomendePostcode_114"])
            mate_van_sted = int(rowdata["MateVanStedelijkheid_116"])
            dict_sted[postcode] = mate_van_sted

    print(df_uniquepeople.shape)

    print("reading GBAPERSOON_trackable_years2018-2022_ext feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_years2018-2022_ext.ftr")

    df_uniquepeople = df_uniquepeople.drop_duplicates(subset = "RINPERSOON")
    print(df_uniquepeople.shape)
    print(df_uniquepeople.head())

    print("dropping non-trackable..")
    df_uniquepeople = df_uniquepeople[  (df_uniquepeople['RINPERSOON'].isin(df_p['RINPERSOON']))  ]
    print(df_uniquepeople.shape)
    print(df_uniquepeople.head())
    # df_p_unique = df_p[  (df_p['RINPERSOON'].isin(df_uniquepeople['RINPERSOON']))  ]

    print("cleaning memory..")
    df_p.iloc[0:0]
    del df_p
    gc.collect()

    size = len(df_uniquepeople["RINPERSOON"])

    # print("processing all selected persons: post_code..")
    post_code_list = [int(0)] * size
    df_uniquepeople["post_code"] = post_code_list
    # for index, rowdata in df_uniquepeople.iterrows():
    #     if index % 1000 == 0:
    #         print(index)
    #     rinp_str = int(rowdata["RINPERSOON"])
    #     rows_p_this = df_s.loc[df_s["RINPERSOON"]==rinp_str]
    #     if len(rows_p_this):
    #         try:
    #             post_code = int(rows_p_this.iloc[0]["GBAPOSTCODE4GAAF1JANUARI"])
    #         except:
    #             post_code = 0
    #     else:
    #         post_code = 0
    #     post_code_list[index] = int(post_code)
    # df_uniquepeople["post_code"] = post_code_list

    print("\nmerging with GBASTANDBEVOLKING\n")
    # start = time.time()
    df_uniquepeople = pd.merge(df_uniquepeople, df_s, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    use_cols = ['RINPERSOON','GBAPOSTCODE4GAAF1JANUARI']
    df_uniquepeople = df_uniquepeople[use_cols]
    print(df_uniquepeople.head())
    print(df_uniquepeople.shape)
    print()

    print("processing all selected persons: region_code..")
    region_code = [int(-1)] * size
    nr_noregion = 0
    for index, rowdata in df_uniquepeople.iterrows():
        if index % 1000 == 0:
            print(index)
        try:
            postcode = int(rowdata["GBAPOSTCODE4GAAF1JANUARI"])  # post_code
            for index2, rowdata2 in df_regios.iterrows():
                postcode_start = int(rowdata2["postcode_start"])
                postcode_end = int(rowdata2["postcode_end"])
                if postcode>=postcode_start and postcode<=postcode_end:
                    region_code[index] = int(rowdata2["provincie_regio_code"])
                    break
        except:
            # print("no valid postcode-regio for:")
            # print(rowdata["RINPERSOON"])
            # print(rowdata["GBAPOSTCODE4GAAF1JANUARI"])
            nr_noregion += 1

    print("nr_noregion: " + str(nr_noregion) )
    df_uniquepeople["region_code"] = region_code

    print()

    print("processing all selected persons: urbanness_level..")
    urbanness_level = [int(-1)] * size
    nr_no_urbanness = 0
    for index, rowdata in df_uniquepeople.iterrows():
        if index % 1000 == 0:
            print(index)
        try:
            postcode = int(rowdata["GBAPOSTCODE4GAAF1JANUARI"])  # post_code
            mate_van_sted = dict_sted[postcode]
            urbanness_level[index] = mate_van_sted
        except:
            # print("no valid postcode-stedelijkheid for:")
            # print(rowdata["RINPERSOON"])
            # print(rowdata["GBAPOSTCODE4GAAF1JANUARI"])
            nr_no_urbanness += 1

    print("nr_no_urbanness: " + str(nr_no_urbanness) )
    df_uniquepeople["urbanness_level"] = urbanness_level

    print(df_uniquepeople.head())

    # use_cols = ['RINPERSOON','RINPERSOONHKW','DEELSCOREWELVAART','DEELSCOREOPLEIDINGSNIVEAU_1','DEELSCORERECENTARBEIDSVERLEDEN','TOTAALSCORE_1']
    # df_uniquepeople = df_uniquepeople[use_cols]

    filename_core =  "selectedpeople_with_urban_region_info_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print("writing: "+filename_ftr)
    # start = time.time()
    df_uniquepeople.to_feather(filename_ftr)
    # print(time.time() - start)
    filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + "_head.csv"
    print("writing: "+filename_csv)
    df_uniquepeople.head(1000).to_csv(filename_csv)
    
if __name__ == '__main__':
    run_main()
    