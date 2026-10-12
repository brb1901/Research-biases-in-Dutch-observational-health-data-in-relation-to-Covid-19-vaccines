import os
import pandas as pd
import time
import argparse

def run_main():
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0"
    # max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    firstyear = 2018
    lastyear = 2021

    code_prefix = "zac_"
    code_str1 = "33238"
    code_str2 = "3323[12345]"

    use_cols = ['RINPERSOON'] #,'zorgactiviteit_list'

    df_out = None
    
    filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_" + code_prefix + str(code_str1) +  versionstr
    # filename_core =  "selectedpeople_" + yearstr + "_zac_" + str(za_code_str) +  versionstr
    filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_core)
    df_indiv = pd.read_feather(filename_ftr)
    df_indiv = df_indiv[use_cols]
    # df_indiv = df_indiv[ (df_indiv["cat"] == 1) ]
    print(df_indiv.shape)        
    df_out = df_indiv

    filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_" + code_prefix + str(code_str2) +  versionstr
    # filename_core =  "selectedpeople_" + yearstr + "_zac_" + str(za_code_str) +  versionstr
    filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_core)
    df_indiv = pd.read_feather(filename_ftr)
    df_indiv = df_indiv[use_cols]
    # df_indiv = df_indiv[ (df_indiv["cat"] == 1) ]
    print(df_indiv.shape) 

    df_out = pd.concat([df_out,df_indiv], ignore_index=True)

    # print(df_out.shape)
    # print(df_out)
    df_out.reset_index(inplace=True,drop=True)
    df_out = df_out.drop_duplicates(subset = "RINPERSOON")
    df_out.reset_index(inplace=True,drop=True)
    print(df_out.shape)

    filename_core =  "selectedpeople_" + str(firstyear) + "_" + str(lastyear) + "_" + code_prefix + str(code_str1) + "_" + str(code_str2) + versionstr
    filename_ftr = basepath_ftr + "selection_zorgpaden/" + filename_core + ".ftr" 
    print("writing: "+filename_ftr)
    # start = time.time()
    df_out.to_feather(filename_ftr)
    # print(time.time() - start)
    filename_csv = basepath_csv + "selection_zorgpaden/" + filename_core + "_head.csv"
    print("writing: "+filename_csv)
    df_out.head(100).to_csv(filename_csv)
    print()


    rinp_ser = df_out["RINPERSOON"].unique()
    nr_rinp = len(rinp_ser)
    print("Number of people with these codes in this period:")
    print(nr_rinp)

    
    
if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("za_code_str")
    # args = parser.parse_args()
    # run_main(args.za_code_str)
    run_main()
    