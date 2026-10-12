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

    # 
    yearSstr =   "2018-2021" # "2021" #

    # filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_" + yearSstr + "_selpeople_" + sel_string + versionstr
    filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_Comorb_" + yearSstr + "_selpeople_" + sel_string + versionstr
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    df_cp= pd.read_feather(filename_ftr)

    df_cp["period0_bit"] = df_cp["year"].astype(int)
    df_cp["period1_bit"] = df_cp["year"].astype(int)
    df_cp["period2_bit"] = df_cp["year"].astype(int)
    df_cp["period3_bit"] = df_cp["year"].astype(int)

    df_cp["period0_bit"] = 0
    df_cp["period1_bit"] = 0
    df_cp["period2_bit"] = 0
    df_cp["period3_bit"] = 0

    print("Adding period0_bit..")
    m = ( (df_cp["year"]==2018) )
    df_cp.loc[m, "period0_bit"] = 1

    print("Adding period1_bit..")
    m = ( (df_cp["year"]==2019) | ((df_cp["year"]==2020) & (df_cp["yearweeknr"]<10)) )
    df_cp.loc[m, "period1_bit"] = 1

    print("Adding period2_bit..")
    m = ( (df_cp["year"]==2020) & (df_cp["yearweeknr"]>=10) )
    df_cp.loc[m, "period2_bit"] = 1

    print("Adding period3_bit..")
    m = ( (df_cp["year"]>2020) )
    df_cp.loc[m, "period3_bit"] = 1

    # filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_PeriodBits_" + yearSstr + "_selpeople_" + sel_string + versionstr
    filename_core =  "carepaths_VektPrestDiag_ZorgAct_EtAl_InclSESWLZ_Comorb_PeriodBits_" + yearSstr + "_selpeople_" + sel_string + versionstr

    # print("Skipping ftr and csv now!")

    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print("writing: "+filename_ftr)
    start = time.time()
    df_cp.to_feather(filename_ftr)
    print(time.time() - start)
    filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + "_head.csv"
    print("writing: "+filename_csv)
    df_cp.head(20800).to_csv(filename_csv)

    filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + ".csv"
    print("writing: "+filename_csv)
    start = time.time()
    df_cp.to_csv(filename_csv)
    print(time.time() - start)

    # print("Skipping dta (Stata) now!")

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sel_string")
    args = parser.parse_args()
    run_main(args.sel_string)
    