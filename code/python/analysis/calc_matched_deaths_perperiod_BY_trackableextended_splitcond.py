import pandas as pd
import argparse
# import time
from generic_functions_calc_deaths_perperiod import calc_deaths_per_period
import matplotlib.pyplot as plt


def run_main(birthyear_from_str, birthyear_to_str, wlz_bit_str, med_rxrisk_scores_str, wlz_levels_str, versionstr):
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    basepath_csv_matched = basepath+"csv/matched/"
    # basepath_ftr_medicijn = basepath+"python_pandas/MEDICIJN/"

    # versionstr = "_v4"
    # refyear = 2021
    birthyear_from = int(birthyear_from_str)
    birthyear_to = int(birthyear_to_str)
    wlz_bit = int(wlz_bit_str)
    # -1: ALL;  0: ONLY med_rxrisk_bin == 0;  1: ONLY med_rxrisk_bin > 0; 
    med_rxrisk_scores = int(med_rxrisk_scores_str) 
    # birthyear_from = 1940 # 1970 # 1950 # 1900 #year - age_to
    # birthyear_to = 1950 #1990 # 1970 # 1950 #year - age_from
    wlz_levels = int(wlz_levels_str)

    weeksteps = 4
    mat_str = "matched"
    # age_from = year - birthyear_to
    # age_to = year - birthyear_from

    filename_core_prefix = "matchedset_trackable_2021_" + "extra1_"
    filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr
    filename_ftr = basepath_ftr_matched+filename_core+".ftr"
    print("reading: " + filename_core)
    df_p = pd.read_feather(filename_ftr)
    print(df_p.shape)

    labelList =[]

    val_interest_str = "med_rxrisk_score_weightedpratt_prevyear"
    # val_interest_str = "WLZ_level"
    print(val_interest_str)
        
    df_p_test = df_p[(df_p['treatment']==1) ]
    hist1 = df_p_test[val_interest_str]
    labelList.append("Vaccinated")

    df_p_test = df_p[(df_p['treatment']==0) ]
    hist0 = df_p_test[val_interest_str]
    labelList.append("Unvaccinated")

    plt.hist([hist1, hist0], density=True, label=labelList, bins=range(-5,30,2))  # med_rxrisk_score_weightedpratt_prevyear
    # plt.hist([hist1, hist0], density=True, label=labelList, bins=range(1,10,1)) # WLZ_level

    plt.xlabel(val_interest_str)
    plt.ylabel('proportion')
    plt.xticks(range(-5,30,2))  # med_rxrisk_score_weightedpratt_prevyear
    # plt.xticks(range(1,10,1))  # WLZ_level
    plt.legend()
    suptitle_str = "Comorbidities hist, age group " + str(birthyear_from) +"-" + str(birthyear_to) +", " + mat_str + versionstr +", WLZ " + str(wlz_bit) +", RxRisk LevelsType " + str(med_rxrisk_scores) + ", WLZ LevelsType " + str(wlz_levels) 
    plt.title(suptitle_str)
    manager = plt.get_current_fig_manager()

    manager.full_screen_toggle()

    figfilestr = "H:/data/output/plots/ves/extra/hist_comorb_" + mat_str + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + versionstr
    plt.savefig(figfilestr + ".pdf", format="pdf", bbox_inches="tight")

    manager.full_screen_toggle()
    plt.show()

    print()
    exit(1)

    calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, versionstr)

    

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
    


 