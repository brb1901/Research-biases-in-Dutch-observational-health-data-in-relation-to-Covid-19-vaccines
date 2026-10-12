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

    # for birthyear in range(2010,1909,-stepsize):
    for birthyear in range(1920,2011,stepsize):
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
            filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr
            filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
            if os.path.exists(filename_ftr):
                print("reading: " + filename_core)
                df_p = pd.read_feather(filename_ftr)                

                wlz_levels = -1
                med_rxrisk_scores = -1
                if wlz_bit==0:
                    for med_rxrisk_scores in [-1,0,1]:
                        calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, versionstr)
                else:
                    for wlz_levels in [-1,0,1]:
                        calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, versionstr)
            else:
                print("file does not exist, skipping this subgroup")
    

if __name__ == '__main__':
    run_main()
    


 