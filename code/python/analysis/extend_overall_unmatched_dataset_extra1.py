import pandas as pd
import argparse
from generic_functions_calc_deaths_perperiod import add_extra_analysis_data
import os


def run_main():
    basepath = "H:/data/"

    versionstr = "_v0"

    # filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead" + versionstr
    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")

    df_p = add_extra_analysis_data(df_p)

    # filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead_extra1" + versionstr
    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead_extra1" + versionstr

    filename_csv = basepath+"csv/GBA/"+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    df_p.head(1000).to_csv(filename_csv)

    filename_ftr = basepath+"python_pandas/GBA/"+filename_core+".ftr"
    print("writing: "+filename_ftr)
    df_p.to_feather(filename_ftr)

    

if __name__ == '__main__':
    run_main()
    


 