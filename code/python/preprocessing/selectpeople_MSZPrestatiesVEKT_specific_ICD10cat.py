import os
import pandas as pd
import time
import argparse

def run_main(cat_string, year_string):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0"
    max_rinp_int_file = 1000000000 # 1 miljard

    year = int(year_string)
    # year = 2018
    RINP_list = []
    file_ID_Prest_list = []
    year_list = []
    quarter_list = []
    koppelIDPrestZa_list_list = []
    ICD10_list_list = []
    zorgtype_list_list = []

    # firstyear = 2018
    # lastyear = 2021

    # df_selection = pd.DataFrame(columns=["RINPERSOON","year","quarter","file_ID_Prest","koppelIDPrestZa_list",
                                        # "ICD10_list","zorgtype_list"])
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
    
    while (final_batch==False & (min_rinp_int <= max_rinp_int_file)):
        min_rinp_int = max_rinp_int+1
        max_rinp_int = min_rinp_int-1 + 1000000 # 1000 #
        
        print(min_rinp_int)
        print(max_rinp_int)
        if min_rinp_int > max_rinp_int_file:
            final_batch = True
            print("Done!")
        else:
            filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
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
                    ICD10_list_str = rowdata["ICD10_list"]   
                    if cat_string in ICD10_list_str:
                        # print(rowdata["RINPERSOON"])
                        nr_people += 1
                        RINP_list.append(rowdata["RINPERSOON"])
                        file_ID_Prest_list.append(rowdata["file_ID_Prest"])
                        year_list.append(rowdata["year"])
                        quarter_list.append(rowdata["quarter"])
                        koppelIDPrestZa_list_list.append(rowdata["koppelIDPrestZa_list"])
                        ICD10_list_list.append(rowdata["ICD10_list"])
                        zorgtype_list_list.append(rowdata["zorgtype_list"])

                #DEBUG
                # final_batch = True
            else:
                print("File does not exist!")
                    
    df_selection["RINPERSOON"] = RINP_list
    df_selection["file_ID_Prest"] = file_ID_Prest_list
    df_selection["year"] = year_list
    df_selection["quarter"] = quarter_list
    df_selection["koppelIDPrestZa_list"] = koppelIDPrestZa_list_list
    df_selection["ICD10_list"] = ICD10_list_list
    df_selection["zorgtype_list"] = zorgtype_list_list

    if df_selection is not None:
        # print(df_out.shape)
        # print(df_out)

        # filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_cat_" + str(cat_string) +  versionstr
        filename_core =  "selectedpeople_" + yearstr + "_cat_" + str(cat_string) +  versionstr
        filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
        print("writing: "+filename_ftr)
        # start = time.time()
        df_selection.to_feather(filename_ftr)
        # print(time.time() - start)
        filename_csv = basepath_csv + "selection_zorgpaden/" + filename_core + "_head.csv"
        print("writing: "+filename_csv)
        df_selection.head(100).to_csv(filename_csv)
        print()
    else:
        print("Empty df_selection!")

    # #DEBUG
    # exit(1)

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cat_string")
    parser.add_argument("year_string")
    args = parser.parse_args()
    run_main(args.cat_string, args.year_string)
    