import pandas as pd
import gc
# import argparse


def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    basepath_ftr_vektis = basepath+"python_pandas/VEKTIS/heartdiag/"
    # basepath_csv_vektis = basepath + "csv/VEKTIS/heartdiag/"

    versionstr = "_v0"
    year = 2021
    versionstr_diag = "_v0"

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead_extra1" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")

    print("selecting only some columns for compact dataset..")
    use_cols = ["RINPERSOON","GBAGESLACHT","GBAGEBOORTEJAAR","GBAGEBOORTEMAAND",
                "WLZ_bit","WLZ_type","WLZ_level","med_rxrisk_score_simplesum_prevyear","med_rxrisk_score_weightedpratt_prevyear",
                "dead_bit","dead_date","dead_cause","covid_vax_firstdate","nr_covid_vax","covid_vax_dates",
                "GBAGEBOORTEJAAR_bin","vaccinated_bit","week_nr_firstvax","year_firstvax","med_rxrisk_score_simplesum_prevyear_bin",
                "med_rxrisk_score_weightedpratt_prevyear_bin","dead_bit_covid","dead_bit_noncovid","week_nr_dead","year_dead",
                "covid_vax_seconddate","covid_vax_thirddate","week_nr_secondvax","year_secondvax","week_nr_thirdvax","year_thirdvax"]
    df_p = df_p[use_cols]

    print("adding some extra analysis data..")
    df_p["treatment"] = 0
    df_p["control"] = 0

    m = ( (df_p["vaccinated_bit"]==1) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
    df_p.loc[m, "treatment"] = 1
    m = ( (df_p["vaccinated_bit"]==0) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
    df_p.loc[m, "control"] = 1

    print(df_p.shape)

    yearstr = str(year)
    # filename_core =  "vektPrest_HeartDiag_ext_myoperiendo_onerowpp_" + yearstr+ versionstr_diag
    filename_core =  "vektPrest_HeartDiag_ext_myocardinfarct_onerowpp_" + yearstr+ versionstr_diag
    print("reading: " + filename_core)
    filename_ftr = basepath_ftr_vektis +filename_core +".ftr"
    print(filename_ftr)

    df_diag = pd.read_feather(filename_ftr)
    print(df_diag.shape)
    print()

    df_diag = df_diag[df_diag['RINPERSOON'].isin(df_p['RINPERSOON'])] # gevaccineerden gevonden in trackable GBA dataset
    print("After removing RIN-PERSONEN not found in trackable GBA dataset:")
    print(df_diag.shape)

    print("\nmerging df_p with df_diag\n")
    # start = time.time()
    df_p = pd.merge(df_p, df_diag, how='left', on=['RINPERSOON'])
    # print(time.time() - start)
    df_p.reset_index(inplace=True,drop=True)
    print(df_p.head())
    print(df_p.shape)

    print("cleaning memory of df_diag..")
    df_diag.iloc[0:0]
    del df_diag
    gc.collect()

    # All WITHOUT the relevant diagnoses
    m = ( (df_p['year_diagnosis'].notnull()==False) )
    # df_p.loc[m, "year_diagnosis"] = -1
    df_p.loc[m, yearstr+"_"+"week1nr"] = -1
    df_p.loc[m, yearstr+"_"+"week2nr"] = -1
    df_p.loc[m, yearstr+"_"+"week3nr"] = -1
    df_p.loc[m, yearstr+"_"+"week4nr"] = -1

    # df_p["year_diagnosis"] = df_p["year_diagnosis"].astype(int)
    df_p.drop(["year_diagnosis"], axis=1, inplace=True)
    df_p[yearstr+"_"+"week1nr"] = df_p[yearstr+"_"+"week1nr"].astype(int)
    df_p[yearstr+"_"+"week2nr"] = df_p[yearstr+"_"+"week2nr"].astype(int)
    df_p[yearstr+"_"+"week3nr"] = df_p[yearstr+"_"+"week3nr"].astype(int)
    df_p[yearstr+"_"+"week4nr"] = df_p[yearstr+"_"+"week4nr"].astype(int)

    # filename_core = "GBAPERSOON_trackable_2021_compact_diag_myoperiendo" + versionstr
    filename_core = "GBAPERSOON_trackable_2021_compact_diag_myocardinfarct" + versionstr

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    # start = time.time()
    df_p.head(1000).to_csv(filename_csv)
    # print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    # start = time.time()
    df_p.to_feather(filename_ftr)
    # print(time.time() - start)


if __name__ == '__main__':
    run_main()
    


 