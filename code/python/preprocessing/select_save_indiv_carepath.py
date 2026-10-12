import os
import pandas as pd
import time
import argparse

def run_main(sel_string):
    basepath =  "H:/data/"
    basepath_ftr_vektis = basepath +"python_pandas/VEKTIS/"
    basepath_csv_vektis = basepath + "csv/VEKTIS/"
    basepath_dta_vektis = basepath + "stata/VEKTIS/"

    versionstr = "_v0"
    df_out = None
    
    year = 2018 # 2019 # 2018 2021 # 

    yearstr = str(year)
    # filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_Comorb_" + yearstr + "_selpeople_" + sel_string + versionstr
    filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_" + yearstr + "_selpeople_" + sel_string + versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 

    print(filename_ftr)
    df_in = pd.read_feather(filename_ftr)

    rinp_str = "455287340"
    df_out = df_in[df_in["RINPERSOON"]==rinp_str] 
    
    # df_out.reset_index(inplace=True,drop=True)
    print(df_out.shape)

    df_out.drop(range(5162508,5162560),axis='index',inplace=True)
    print(df_out.shape)

    # print("Sorting..")
    # df_out.sort_values(by=["RINPERSOON", "year", "yearweeknr"], inplace=True) # 
    # df_out.reset_index(inplace=True,drop=True)
    # print()

    versionstr = "_v0b"
    # filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_Comorb_" + yearstr + "_sel_" + rinp_str + versionstr
    filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_" + yearstr + "_sel_" + rinp_str + versionstr

    # print("Skipping ftr and csv now!")

    # filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    # print("writing: "+filename_ftr)
    # start = time.time()
    # df_out.to_feather(filename_ftr)
    # print(time.time() - start)
    # filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + "_head.csv"
    # print("writing: "+filename_csv)
    # df_out.head(5000).to_csv(filename_csv)

    filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + ".csv"
    print("writing: "+filename_csv)
    start = time.time()
    df_out.to_csv(filename_csv)
    print(time.time() - start)

    # print("Skipping dta (Stata) now!")

    # df_out["dead_date_str"] = df_out["dead_date"].astype(str)  # .dt.strftime("%Y-%m-%d")
    # df_out["covid_pos_test_date_str"] = df_out["covid_pos_test_date"].astype(str)  # .dt.strftime("%Y-%m-%d")
    # df_out["covid_vax_date_str"] = df_out["covid_vax_date"].astype(str)  # .dt.strftime("%Y-%m-%d")
    # df_out["nonacute_ZA_date_str"] = df_out["nonacute_ZA_date"].astype(str)  # .dt.strftime("%Y-%m-%d")
    # df_out["acute_ZA_date_str"] = df_out["acute_ZA_date"].astype(str)  # .dt.strftime("%Y-%m-%d")
    # # df_out["dead_date_str"] = df_out["dead_date"].dt.strftime("%Y-%m-%d")
    # df_out.drop(["dead_date","covid_pos_test_date","covid_vax_date","nonacute_ZA_date","acute_ZA_date"], axis=1, inplace=True)
    # filename_dta = basepath_dta_vektis + "selection_zorgpaden/" +filename_core + ".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_out.to_stata(filename_dta, version=117)
    # print(time.time() - start)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sel_string")
    args = parser.parse_args()
    run_main(args.sel_string)
    