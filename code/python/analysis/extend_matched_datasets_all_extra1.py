import pandas as pd
import argparse
from generic_functions_calc_deaths_perperiod import add_extra_analysis_data
import os


def run_main():
    basepath = "H:/data/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    basepath_csv_matched = basepath+"csv/matched/"

    filename_core_prefix = "matchedset_trackable_2021_"
    filename_core_prefix_new = filename_core_prefix + "extra1_"
    # mat_str = "unmatched"
    # weeksteps = 4
    stepsize = 10
    versionstr = "_v3"

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
            filename_ftr = basepath_ftr_matched+filename_core+".ftr"
            if os.path.exists(filename_ftr):
                print("reading: " + filename_core)
                df_p = pd.read_feather(filename_ftr)

                df_p = add_extra_analysis_data(df_p)

                filename_core = filename_core_prefix_new + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr

                filename_csv = basepath_csv_matched+filename_core+"_head.csv"
                print("writing (head): "+filename_csv)
                df_p.head(1000).to_csv(filename_csv)

                filename_ftr = basepath_ftr_matched+filename_core+".ftr"
                print("writing: "+filename_ftr)
                df_p.to_feather(filename_ftr)
            else:
                print("file does not exist, skipping this subgroup")
    

if __name__ == '__main__':
    run_main()
    


 