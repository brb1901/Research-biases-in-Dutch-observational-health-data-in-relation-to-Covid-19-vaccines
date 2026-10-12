import os
import pandas as pd
import time
import argparse
# import re
import gc
from datetime import date, datetime



def make_extend_df_out(df_indiv, df_out, pers_i):
    if pers_i == 0:
        df_out = df_indiv
    else:
        df_out = pd.concat([df_out,df_indiv], ignore_index=True)
        # df_out.append(df_indiv)
        df_out.reset_index(inplace=True,drop=True)
    return df_out


def get_date_from_quarter_excl(year, yq, to_bool=True):
    match yq:
        case 1:
            if to_bool:
                dt = date(year,4,1)
            else:
                dt = date(year,1,1)
        case 2:
            if to_bool:
                dt = date(year,7,1)
            else:
                dt = date(year,4,1)
        case 3:
            if to_bool:
                dt = date(year,10,1)
            else:
                dt = date(year,7,1)
        case 4:
            if to_bool:
                dt = date(year+1,1,1)
            else:
                dt = date(year,10,1)
        case _:
            dt = None
    return dt


def process_person(rinp_str, df_input, year, df_o_year, df_o_2022, df_do):
    df_indiv = df_input.copy()
    dead = False
    dead_post_list = [int(0)] * 4
    dead_yq_list = [int(0)] * 4
    dead_date_list = [None] * 4
    dead_cause_list = [None] * 4
    dead_place_list = [int(0)] * 4
    dead_date = None
    df_fo = df_o_year[ (df_o_year["RINPERSOON"] == rinp_str) ]
    dead_yq = -1
    if len(df_fo): # dus deze persoon is dood, in dit jaar
        for yq in [1,2,3,4]:
            # print(yq)
            if dead: # from before
                dead_yq_list[yq-1] = 1
            else:
                date_from = get_date_from_quarter_excl(year, yq, False)
                date_to = get_date_from_quarter_excl(year, yq, True)
                rows = df_fo.loc[ (df_fo["datetimeobj_overlijden"]>=date_from) & (df_fo["datetimeobj_overlijden"]<date_to) ]
                if len(rows):
                    dead_date = rows.iloc[0]["datetimeobj_overlijden"]
                    dead = True
                    dead_yq_list[yq-1] = 1
                    dead_date_list[yq-1] = dead_date
                    print(rinp_str)
                    print(dead_date)
                    dead_yq = yq
                    rows = df_do.loc[ (df_do["RINPERSOON"] == rinp_str) ]
                    if len(rows):
                        dead_cause = rows.iloc[0]["UCCODE"]
                        plovl = rows.iloc[0]["PLOVL"]                     
                        print(dead_cause)
                        print(plovl)
                        dead_cause_list[yq-1] = dead_cause
                        dead_place_list[yq-1] = int(plovl)
    
    if not dead and year == 2021: 
        df_fo = df_o_2022[ (df_o_2022["RINPERSOON"] == rinp_str) ]
        if len(df_fo): # dus deze persoon is dood, in het jaar 2022
            date_from = get_date_from_quarter_excl(2022, 1, False)
            date_to = get_date_from_quarter_excl(2022, 4, True)
            rows = df_fo.loc[ (df_fo["datetimeobj_overlijden"]>=date_from) & (df_fo["datetimeobj_overlijden"]<date_to) ]
            if len(rows):
                dead_date = rows.iloc[0]["datetimeobj_overlijden"]
                dead = True
                dead_yq_list[3] = 1
                dead_date_list[3] = dead_date
                dead_post_list[3] = 1
                print(rinp_str)
                print(dead_date)
                dead_yq = 5
                rows = df_do.loc[ (df_do["RINPERSOON"] == rinp_str) ]
                if len(rows):
                    dead_cause = rows.iloc[0]["UCCODE"]
                    plovl = rows.iloc[0]["PLOVL"]                     
                    print(dead_cause)
                    print(plovl)
                    dead_cause_list[3] = dead_cause
                    dead_place_list[3] = int(plovl)        
    
    df_indiv["dead"] = dead_yq_list
    df_indiv["dead_post"] = dead_post_list
    df_indiv["dead_date"] = dead_date_list   
    df_indiv["dead_cause"] = dead_cause_list    
    df_indiv["dead_place"] = dead_place_list     

    return [dead, df_indiv, dead_yq]


def run_main(zacode_string, year_string):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    max_rinp_int_file = 1000000000 # 1 miljard

    year = int(year_string)
    firstyear = 2018
    lastyear = 2021

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    df_o_year = df_o[ (df_o["jaar_overlijden"] == year) ] # alle doden in dat jaar
    print("Number of people who died this year: " + str(len(df_o_year)))
    df_o_2022 = df_o[ (df_o["jaar_overlijden"] == 2022) ] # alle doden in dat jaar
    print("Number of people who died in 2022: " + str(len(df_o_2022)))

    print("reading GBAPERSOON_trackable_years2018-2022_ext feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_years2018-2022_ext.ftr")

    filename_core = "DOODOORZ2015-2022" 
    print("reading " + filename_core + " feather data")
    df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

    versionstr = "_v0"
    filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_zac_" + str(zacode_string) +  versionstr
    filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)

    file_exists = os.path.exists(filename_ftr)
    if file_exists:
        print("reading " + filename_ftr)
        df_in = pd.read_feather(filename_ftr)
        print(df_in.shape)
        df_uniquepeople = df_in.drop_duplicates(subset = "RINPERSOON")
        print(df_uniquepeople.shape)

        print("dropping non-trackable..")
        df_uniquepeople = df_uniquepeople[  (df_uniquepeople['RINPERSOON'].isin(df_p['RINPERSOON']))  ]
        print(df_uniquepeople.shape)

        df_p.iloc[0:0]
        del df_p
        gc.collect()
    else:
        print("File does not exist!")
        exit(1)

    # df_selection = pd.DataFrame(columns=["RINPERSOON","year","quarter","file_ID_Prest","koppelIDPrestZa_list",
                                        # "ICD10_list","zorgtype_list"])

    # use_cols = ['RINPERSOON',"year","quarter","file_ID_ZorgAct","nr_Act","zorgactiviteit_list","zorgtypecode_list","zorgactiviteit_int_list"]
    # df_selection = pd.DataFrame()

    # final_batch = False
    # nr_people = 0
    # for year in [2018, 2019, 2020, 2021]:
    yearstr = str(year)
    print(year)

    max_rinp_int = 0
    min_rinp_int = 1
    #DEBUG:
    final_batch = False

    versionstr = "_v0B"

    # nr_q_dict = {1: 0, 2: 0, 3: 0, 4: 0}
    nr_dead_q_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    # prop_dead_q_dict = {1: 0, 2: 0, 3: 0, 4: 0}
    df_out = None
    pers_i = 0
    while (final_batch==False & (min_rinp_int <= max_rinp_int_file)):
        min_rinp_int = max_rinp_int+1
        max_rinp_int = min_rinp_int-1 + 1000000 # 1000 #
        
        print(min_rinp_int)
        print(max_rinp_int)
        if min_rinp_int > max_rinp_int_file:
            final_batch = True
            print("Done!")
        else:
            filename_core = "VEKTIS_ZorgActPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
            filename_ftr = basepath_ftr + filename_core + ".ftr" 

            file_exists = os.path.exists(filename_ftr)
            if file_exists:
                print("reading " + filename_ftr)
                df_za = pd.read_feather(filename_ftr)
                # print(df_indiv.shape)
                df_in = df_za[df_za['RINPERSOON'].isin(df_uniquepeople['RINPERSOON'])] 

                rinp_ser = df_in["RINPERSOON"].unique()
                nr_rinp = len(rinp_ser)
                print("Number of people in this batch:")
                print(nr_rinp)
                
                # if nr_rinp < 30:
                #     maxrange = nr_rinp
                # else:
                #     maxrange = 30
                for i in range(nr_rinp): # range(10): #range(nr_rinp): maxrange
                    if i % 100 == 0 and i!=0:
                        print(i)
                        # if i == 5000:
                        #     exit(1)
                    rinp_str = rinp_ser[i]
                    # print(rinp_str)
                    df_indiv = df_in[df_in['RINPERSOON']==rinp_str]
                    [dead, df_indiv, dead_yq] = process_person(rinp_str, df_indiv, year, df_o_year, df_o_2022, df_do)
                    if dead and dead_yq>-1:
                        nr_dead_q_dict[dead_yq] += 1
                    
                    # print(df_indiv)
                    df_out = make_extend_df_out(df_indiv, df_out, pers_i)
                    pers_i += 1

                #DEBUG
                # final_batch = True
            else:
                print("File does not exist!")
                    
    print(pers_i)
    print(nr_dead_q_dict)

    if df_out is not None:
        # print(df_out.shape)
        # print(df_out)

        versionstr = "_v0"
        # filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_cat_" + str(zacode_string) +  versionstr
        filename_core =  "za_YQ_withdeath_data_selectedpeople_" + yearstr + "_zac_" + str(zacode_string) +  versionstr
        filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
        print("writing: "+filename_ftr)
        # start = time.time()
        df_out.to_feather(filename_ftr)
        # print(time.time() - start)
        filename_csv = basepath_csv + "selection_zorgpaden/" + filename_core + "_head.csv"
        print("writing: "+filename_csv)
        df_out.head(1000).to_csv(filename_csv)
        print()
    else:
        print("Empty df_out!")

    # #DEBUG
    # exit(1)

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("zacode_string")
    parser.add_argument("year_string")
    args = parser.parse_args()
    run_main(args.zacode_string, args.year_string)
    