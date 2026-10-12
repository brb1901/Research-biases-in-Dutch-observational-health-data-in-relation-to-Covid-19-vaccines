import os
import pandas as pd
import time
import argparse
import re

def run_main(zacode_string, year_string):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0B"
    max_rinp_int_file = 1000000000 # 1 miljard

    year = int(year_string)
    # year = 2018
    RINP_list = []
    file_ID_ZorgAct_list = []
    year_list = []
    quarter_list = []
    nr_Act_list = []
    zorgactiviteit_list_list = []
    zorgactiviteit_int_list_list = []
    zorgtypecode_list_list = []

    # firstyear = 2018
    # lastyear = 2021

    # df_selection = pd.DataFrame(columns=["RINPERSOON","year","quarter","file_ID_Prest","koppelIDPrestZa_list",
                                        # "ICD10_list","zorgtype_list"])

    # use_cols = ['RINPERSOON',"year","quarter","file_ID_ZorgAct","nr_Act","zorgactiviteit_list","zorgtypecode_list","zorgactiviteit_int_list"]
    df_selection = pd.DataFrame()

    final_batch = False
    nr_people = 0
    # for year in [2018, 2019, 2020, 2021]:
    yearstr = str(year)
    print(year)

    max_rinp_int = 0
    min_rinp_int = 1
    #DEBUG:
    final_batch = False

    nr_q_dict = {1: 0, 2: 0, 3: 0, 4: 0}
    
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
                df_indiv = pd.read_feather(filename_ftr)
                # print(df_indiv.shape)

                for index, rowdata in df_indiv.iterrows():
                    if index % 10000 == 0 and index!=0:
                        print(index)
                        print("nr_people " + str(nr_people))
                    zorgactiviteit_list_str = rowdata["zorgactiviteit_list"]   
                    # regex_str = rowdata_comorb["regex_atc4_approx"]
                    match_regex = re.search(zacode_string, zorgactiviteit_list_str)
                    # if zacode_string in zorgactiviteit_list_str:
                    if match_regex:
                        # print(rowdata["RINPERSOON"])
                        nr_people += 1
                        RINP_list.append(rowdata["RINPERSOON"])
                        file_ID_ZorgAct_list.append(rowdata["file_ID_ZorgAct"])
                        year_list.append(rowdata["year"])
                        quarter_list.append(rowdata["quarter"])
                        nr_Act_list.append(rowdata["nr_Act"])
                        zorgactiviteit_list_list.append(rowdata["zorgactiviteit_list"])
                        zorgactiviteit_int_list_list.append(rowdata["zorgactiviteit_int_list"])
                        zorgtypecode_list_list.append(rowdata["zorgtypecode_list"])
                        q= int(rowdata["quarter"])
                        nr_q_dict[q] += 1
                        # print(zorgactiviteit_list_str)
                        # exit(1)

                #DEBUG
                # final_batch = True
            else:
                print("File does not exist!")
                    
    df_selection["RINPERSOON"] = RINP_list
    df_selection["file_ID_ZorgAct"] = file_ID_ZorgAct_list
    df_selection["year"] = year_list
    df_selection["quarter"] = quarter_list
    df_selection["nr_Act"] = nr_Act_list
    df_selection["zorgactiviteit_list"] = zorgactiviteit_list_list
    df_selection["zorgtypecode_list"] = zorgtypecode_list_list
    df_selection["zorgactiviteit_int_list"] = zorgactiviteit_int_list_list

    print(nr_q_dict)

    # if df_selection is not None:
    #     # print(df_out.shape)
    #     # print(df_out)

    #     versionstr = "_v0"
    #     # filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_cat_" + str(zacode_string) +  versionstr
    #     filename_core =  "selectedpeople_" + yearstr + "_zac_" + str(zacode_string) +  versionstr
    #     filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
    #     print("writing: "+filename_ftr)
    #     # start = time.time()
    #     df_selection.to_feather(filename_ftr)
    #     # print(time.time() - start)
    #     filename_csv = basepath_csv + "selection_zorgpaden/" + filename_core + "_head.csv"
    #     print("writing: "+filename_csv)
    #     df_selection.head(100).to_csv(filename_csv)
    #     print()
    # else:
    #     print("Empty df_selection!")

    # #DEBUG
    # exit(1)

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("zacode_string")
    parser.add_argument("year_string")
    args = parser.parse_args()
    run_main(args.zacode_string, args.year_string)
    