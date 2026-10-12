import pandas as pd
import argparse
from generic_functions_calc_deaths_perperiod import calc_deaths_per_period


def run_main(birthyear_from_str, birthyear_to_str, wlz_bit_str, med_rxrisk_scores_str, wlz_levels_str, versionstr):
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    # basepath_ftr_medicijn = basepath+"python_pandas/MEDICIJN/"
    basepath_ftr_vektis = basepath+"python_pandas/VEKTIS/"

    # versionstr = "_v0"
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
    mat_str = "unmatched_dotter"

    # age_from = year - birthyear_to
    # age_to = year - birthyear_from

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead_extra1" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")


    versionstr_dotter = "_v0"
    sel_string = "zac_33238_3323[12345]"
    firstyear = 2018
    lastyear = 2021
    # yearSstr =   "2018-2021" # "2021" #

    filename_core =  "selectedpeople_sorted_with_urban_region_info_" + str(firstyear) + "_" + str(lastyear) + "_" + str(sel_string) +  versionstr_dotter
    filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
    print(filename_ftr)
    df_uniquepeople = pd.read_feather(filename_ftr)
    print(df_uniquepeople.shape)

    print("SELECTING DOTTER PATIENTS!")
    df_p = df_p[ (df_p['RINPERSOON'].isin(df_uniquepeople['RINPERSOON'])) ]
    print()

    print("adding some extra analysis data..")
    df_p["treatment"] = 0
    df_p["control"] = 0
    df_p["week_nr_dead"] = -1
    df_p["year_dead"] = -1

    m = ( (df_p["vaccinated_bit"]==1) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
    df_p.loc[m, "treatment"] = 1
    m = ( (df_p["vaccinated_bit"]==0) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
    df_p.loc[m, "control"] = 1

    m = ( (df_p["dead_bit"]==1) )
    df_p.loc[m, "week_nr_dead"] = df_p.loc[m, "dead_date"].dt.isocalendar().week
    df_p.loc[m, "year_dead"] = df_p.loc[m, "dead_date"].dt.isocalendar().year

    # # for year in [2018, 2019, 2020, 2021, 2022]:
    # year = 2021 # 2019 # 2018 2021 # 
    # year_tostop = 2024 #2022 #  
    # nr_years = year_tostop - year
    # # 
    # yearsstr = "2021-2023" # "2021" #"2019-2022" # 
    # year_prev = year - 1
    
    # print("First year:")
    # print(year)

    # age_from = 70 # 50 # 15 # 65 # 10 # 15 # 60 50 40 # 
    # age_to = 125 # 65 # 50 # 125 # 50 # 45 # 90 75 65 # 

    df_p = df_p[ (df_p['WLZ_bit']==wlz_bit) ] # &  ((df_p['jaar_overlijden']>=year) | (df_p['jaar_overlijden']==-1))
    print(df_p.shape)

    val_interest_str = "GBAGEBOORTEJAAR"
    print(val_interest_str)
    median_val = df_p[val_interest_str].median()
    print("median_val: " + str(median_val))
    mean_val = df_p[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    percentile90_val = df_p[val_interest_str].quantile(0.9)
    print("percentile90_val: " + str(percentile90_val))
    print()

    
    df_p_test = df_p[(df_p['treatment']==1) ]
    print("treatment: " + str(1) )
    val_interest_str = "GBAGEBOORTEJAAR"
    print(val_interest_str)
    median_val = df_p_test[val_interest_str].median()
    print("median_val: " + str(median_val))
    mean_val = df_p_test[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    percentile90_val = df_p_test[val_interest_str].quantile(0.9)
    print("percentile90_val: " + str(percentile90_val))
    val_interest_str = "med_rxrisk_score_weightedpratt_prevyear"
    print(val_interest_str)
    median_val = df_p_test[val_interest_str].median()
    print("median_val: " + str(median_val))
    mean_val = df_p_test[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    percentile90_val = df_p_test[val_interest_str].quantile(0.9)
    print("percentile90_val: " + str(percentile90_val))
    print()

    df_p_test = df_p[(df_p['treatment']==0) ]
    print("treatment: " + str(0) )
    val_interest_str = "GBAGEBOORTEJAAR"
    print(val_interest_str)
    median_val = df_p_test[val_interest_str].median()
    print("median_val: " + str(median_val))
    mean_val = df_p_test[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    percentile90_val = df_p_test[val_interest_str].quantile(0.9)
    print("percentile90_val: " + str(percentile90_val))
    val_interest_str = "med_rxrisk_score_weightedpratt_prevyear"
    print(val_interest_str)
    median_val = df_p_test[val_interest_str].median()
    print("median_val: " + str(median_val))
    mean_val = df_p_test[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    percentile90_val = df_p_test[val_interest_str].quantile(0.9)
    print("percentile90_val: " + str(percentile90_val))
    print()


    print()
    
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
    


 