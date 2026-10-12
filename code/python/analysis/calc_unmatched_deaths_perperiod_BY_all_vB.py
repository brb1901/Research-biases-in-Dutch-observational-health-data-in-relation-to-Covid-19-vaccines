import pandas as pd
import argparse
from generic_functions_calc_deaths_perperiod import calc_deaths_per_period
import os


def run_main():
    basepath = "H:/data/"
    basepath_ftr_unmatched = basepath+"python_pandas/unmatched/"
    # basepath_csv_unmatched = basepath+"csv/unmatched/"

    filename_core_prefix = "unmatchedset_trackable_2021_" + "extra1_"
    mat_str = "unmatched"
    weeksteps = 4
    stepsize = 10
    versionstr = "_v0"

    out_versionstr = versionstr+"E"

    # for birthyear in range(2010,1909,-stepsize):

    # for birthyear in range(1920,2001,stepsize):
    for birthyear in [1920,1930,1940,1950,1960,1980,2000]: #1920,1930,1940,
    # for birthyear in range(1920,1921,stepsize):
    # for birthyear in range(2000,2001,stepsize):
    # stepsize = 100
    # for birthyear in range(1910,2009,stepsize):
        birthyear_from = birthyear
        birthyear_to = birthyear_from + stepsize
        # age_from = refyear - birthyear_to
        # age_to = refyear - birthyear_from
        print(birthyear_from)
        print(birthyear_to)
        print()

        for wlz_bit in [0,1]:
            print(wlz_bit)
            ok_bit = True
            if birthyear_from>=1960: # ==2000
                print("20 YEARS")
                birthyear_from_temp = birthyear_from
                birthyear_to_temp = birthyear_from_temp + stepsize
                filename_core = filename_core_prefix + str(birthyear_from_temp) + "_" + str(birthyear_to_temp) + "_WLZ" + str(wlz_bit) + versionstr
                filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
                if os.path.exists(filename_ftr):
                    print("reading: " + filename_core)
                    df_p1 = pd.read_feather(filename_ftr)     
                else:
                    ok_bit = False
                if ok_bit:
                    birthyear_from_temp = birthyear_to_temp
                    birthyear_to_temp = birthyear_from_temp + stepsize
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
                    birthyear_to = birthyear_from+20
                    print("20 YEARS SUCCESS")

            else:
                filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr
                filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
                if os.path.exists(filename_ftr):
                    print("reading: " + filename_core)
                    df_p = pd.read_feather(filename_ftr)     
                else:
                    ok_bit = False

            # if birthyear_from>=1960:
            #     weeksteps = 13
            # else:
            #     weeksteps = 4

            if ok_bit:  
                wlz_levels = -1
                med_rxrisk_scores = -1
                if wlz_bit==0:
                    if birthyear_from==1940 or birthyear_from==1960 or birthyear_from==1980:
                        for med_rxrisk_scores in [-1,0,1]:
                            calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, out_versionstr)
                    else:
                        med_rxrisk_scores=-1
                        calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, out_versionstr)
                else:
                    if birthyear_from==1930:
                        for wlz_levels in [-1,0,1]:
                            calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, out_versionstr)
                    else:
                        wlz_levels=-1
                        calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, out_versionstr)
            else:
                print("file does not exist, skipping this subgroup")
    

if __name__ == '__main__':
    run_main()
    


 