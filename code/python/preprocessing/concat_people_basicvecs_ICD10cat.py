import os
import pandas as pd
import time
import argparse

def run_main(cat_string):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0"
    max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    # year = int(year_string)
    # year = 2018
    # 
    # yearstr = str(year)
    # print(year)
    firstyear = 2018
    lastyear = 2021

    # use_cols = ['RINPERSOON',"year","quarter","file_ID_Prest"]

    max_rinp_int = 0
    min_rinp_int = 1
    final_batch = False
    df_out = None
    while (min_rinp_int <= max_rinp_int_file) and ~final_batch:
        min_rinp_int = max_rinp_int+1
        max_rinp_int = min_rinp_int-1 + 1000000 # 1000 #
        
        print(min_rinp_int)
        print(max_rinp_int)
        if min_rinp_int > max_rinp_int_file:
            final_batch = True
            print("Done!")
        else:
            for year in [2018, 2019, 2020, 2021]:
                yearstr = str(year)   
                # print(yearstr) 
                filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_cat_" + str(cat_string) + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
                print(filename_core)
                filename_ftr = basepath_ftr + "morbid/" + filename_core + ".ftr" 
                file_exists = os.path.exists(filename_ftr)
                if file_exists: # True: # 
                    df_indiv = pd.read_feather(filename_ftr)
                    df_indiv = df_indiv[ (df_indiv["cat"] == 1) ]
                    print(df_indiv.shape)
                    if df_out is None:
                        df_out = df_indiv
                    else:
                        df_out = pd.concat([df_out,df_indiv], ignore_index=True)                           
                        # df_out.reset_index(inplace=True,drop=True)

                    
    if df_out is not None:
        # print(df_out.shape)
        # print(df_out)
        df_out.reset_index(inplace=True,drop=True)

        filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + str(firstyear) + "_" + str(lastyear) + "_" + "people_cat_" + str(cat_string) +  versionstr
        filename_ftr = basepath_ftr + "cat_collections/" + filename_core + ".ftr" 
        print("writing: "+filename_ftr)
        # start = time.time()
        df_out.to_feather(filename_ftr)
        # print(time.time() - start)
        filename_csv = basepath_csv + "cat_collections/" + filename_core + "_head.csv"
        print("writing: "+filename_csv)
        df_out.head(100).to_csv(filename_csv)
        print()
    else:
        print("Empty df_out!")

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cat_string")
    args = parser.parse_args()
    run_main(args.cat_string)
    