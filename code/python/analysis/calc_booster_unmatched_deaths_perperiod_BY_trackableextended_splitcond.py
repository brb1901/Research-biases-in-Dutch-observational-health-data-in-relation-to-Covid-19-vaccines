import pandas as pd
import argparse
from generic_functions_calc_deaths_perperiod import calc_deaths_per_period
import os
import time
import math

   

def run_main(birthyear_from_str, birthyear_to_str, wlz_bit_str, med_rxrisk_scores_str, wlz_levels_str, versionstr):
    basepath = "H:/data/"
    basepath_ftr_unmatched = basepath+"python_pandas/unmatched/"
    # basepath_csv_unmatched = basepath+"csv/unmatched/"

    filename_core_prefix = "unmatchedset_trackable_2021_" +  "extra1_"
    mat_str = "unmatched"
    weeksteps = 4
    birthyear_from = int(birthyear_from_str)
    birthyear_to = int(birthyear_to_str)
    wlz_bit = int(wlz_bit_str)
    # -1: ALL;  0: ONLY med_rxrisk_bin == 0;  1: ONLY med_rxrisk_bin > 0; 
    med_rxrisk_scores = int(med_rxrisk_scores_str) 
    # birthyear_from = 1940 # 1970 # 1950 # 1900 #year - age_to
    # birthyear_to = 1950 #1990 # 1970 # 1950 #year - age_from
    wlz_levels = int(wlz_levels_str)
    
    out_versionstr = versionstr+"E"

    ok_bit = True

    birthyear_diff = birthyear_to - birthyear_from
    if birthyear_diff==20:
        print("20 YEARS")
        birthyear_from_temp = birthyear_from
        birthyear_to_temp = birthyear_from_temp + 10
        filename_core = filename_core_prefix + str(birthyear_from_temp) + "_" + str(birthyear_to_temp) + "_WLZ" + str(wlz_bit) + versionstr
        filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
        if os.path.exists(filename_ftr):
            print("reading: " + filename_core)
            df_p1 = pd.read_feather(filename_ftr)     
        else:
            ok_bit = False
        if ok_bit:
            birthyear_from_temp = birthyear_to_temp
            birthyear_to_temp = birthyear_from_temp + 10
            filename_core = filename_core_prefix + str(birthyear_from_temp) + "_" + str(birthyear_to_temp) + "_WLZ" + str(wlz_bit) + versionstr
            filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
            if os.path.exists(filename_ftr):
                print("reading: " + filename_core)
                df_p2 = pd.read_feather(filename_ftr)     
            else:
                ok_bit = False
        if ok_bit:
            df_p = pd.concat([df_p1,df_p2], ignore_index=True)
            df_p.reset_index(inplace=True,drop=True)
        
    elif birthyear_diff==10:
        filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr
        filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
        if os.path.exists(filename_ftr):
            print("reading: " + filename_core)
            df_p = pd.read_feather(filename_ftr)
        else:
            ok_bit = False

    if ok_bit:
        # df_p = add_extra_analysis_data(df_p)
        df_p["treatment"] = 0
        df_p["control"] = 0

        m = ( ((df_p["year_thirdvax"] == 2021) & (df_p["week_nr_thirdvax"] >= 40)) 
             | ((df_p["year_thirdvax"] == 2022) & (df_p["week_nr_thirdvax"] <= 18))  ) # BOOSTER DEF
        df_p.loc[m, "treatment"] = 1
        m = ( (df_p["treatment"]==0) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
        df_p.loc[m, "control"] = 1

        calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, out_versionstr, booster=True)
    else:
        print("file does not exist, skipping this subgroup")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("birthyear_from_str")
    parser.add_argument("birthyear_to_str")
    parser.add_argument("wlz_bit_str")
    parser.add_argument("med_rxrisk_scores_str")
    parser.add_argument("wlz_levels_str")
    parser.add_argument("versionstr")
    args = parser.parse_args()
    run_main(args.birthyear_from_str, args.birthyear_to_str, args.wlz_bit_str, args.med_rxrisk_scores_str,
             args.wlz_levels_str, args.versionstr)
    


 