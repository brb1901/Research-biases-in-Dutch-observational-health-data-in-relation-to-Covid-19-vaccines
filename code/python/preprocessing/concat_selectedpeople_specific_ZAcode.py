import os
import pandas as pd
import time
import argparse

def run_main(za_code_str):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0"
    # max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    firstyear = 2018
    lastyear = 2021

    df_out = None
    for year in [2018, 2019, 2020, 2021]:
        yearstr = str(year)   
        # print(yearstr) 
        filename_core =  "selectedpeople_" + yearstr + "_zac_" + str(za_code_str) +  versionstr
        filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
        print(filename_core)
        file_exists = os.path.exists(filename_ftr)
        if file_exists: # True: # 
            df_indiv = pd.read_feather(filename_ftr)
            # df_indiv = df_indiv[ (df_indiv["cat"] == 1) ]
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

        filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_zac_" + str(za_code_str) +  versionstr
        filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
        print("writing: "+filename_ftr)
        # start = time.time()
        df_out.to_feather(filename_ftr)
        # print(time.time() - start)
        filename_csv = basepath_csv + "selection_zorgpaden/" + filename_core + "_head.csv"
        print("writing: "+filename_csv)
        df_out.head(100).to_csv(filename_csv)
        print()
    else:
        print("Empty df_out!")

    rinp_ser = df_out["RINPERSOON"].unique()
    nr_rinp = len(rinp_ser)
    print("Number of people with this ZA code in this period:")
    print(nr_rinp)

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("za_code_str")
    args = parser.parse_args()
    run_main(args.za_code_str)
    