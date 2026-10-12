import os
import pandas as pd
import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
# import argparse
# from lifelines import KaplanMeierFitter


def analyze(df_p, vaxed, dead, birthyear_from, birthyear_to, bothvaxstatuses, bothdeadstatuses):
    print("vaxed: " + str(vaxed) + " dead: " + str(dead))
    print("bothvaxstatuses: " + str(bothvaxstatuses) + " bothdeadstatuses: " + str(bothdeadstatuses))
    if bothdeadstatuses:
        df_p = df_p[ (df_p['nr_covid_vax'].notnull()==vaxed) 
                    & (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) ]
    else:
        if bothvaxstatuses:
            df_p = df_p[ (df_p['dead_bit']==dead) 
                    & (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) ]
        else:
            df_p = df_p[ (df_p['nr_covid_vax'].notnull()==vaxed) & (df_p['dead_bit']==dead) 
                    & (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) ]
    print(len(df_p))

    val_interest_str = "med_rxrisk_score_weightedpratt_prevyear" # "med_rxrisk_score_simplesum_prevyear"
    median_val = df_p[val_interest_str].median()
    print("median_val: " + str(median_val))
    mean_val = df_p[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    percentile90_val = df_p[val_interest_str].quantile(0.9)
    print("percentile90_val: " + str(percentile90_val))
    print()

    df_p.hist(column=[val_interest_str], grid = False)
    plt.xlabel(val_interest_str)
    # plt.savefig("H:/data/output/plots/" + val_interest_str + "_hist_" + labeltext + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show()


def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    versionstr = "_v0"

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    birthyear_from = 1930
    birthyear_to = birthyear_from + 20
    print(str(birthyear_from) + "-" + str(birthyear_to))

    bothvaxstatuses = False
    bothdeadstatuses = True

    vaxed =True
    dead = 1
    analyze(df_p, vaxed, dead, birthyear_from, birthyear_to, bothvaxstatuses, bothdeadstatuses)

    vaxed =False
    dead = 1
    analyze(df_p, vaxed, dead, birthyear_from, birthyear_to, bothvaxstatuses, bothdeadstatuses)
    
if __name__ == '__main__':
    run_main()
    