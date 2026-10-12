import pandas as pd
import time
# from datetime import date
import gc
import math
import os

def run_main():
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    # basepath_ftr_medicijn = basepath+"python_pandas/MEDICIJN/"

    versionstr = "_v0"
    # refyear = 2021

    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ_ComorbMed_Dead_Vax" + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    df_p["dead_date"] = pd.to_datetime(df_p["dead_date"])
    df_p["covid_vax_firstdate"] = pd.to_datetime(df_p["covid_vax_firstdate"])

    df_p["GBAGEBOORTEJAAR_bin"] = -1
    df_p["vaccinated_bit"] = -1
    df_p["week_nr_firstvax"] = -1
    df_p["year_firstvax"] = -1

    # df_p["nr_Med_prevyear_bin"] = -1
    df_p["med_rxrisk_score_simplesum_prevyear_bin"] = -1
    df_p["med_rxrisk_score_weightedpratt_prevyear_bin"] = -1

    print("Set vaccinated_bit and week number of first vaccination")
    # All vaccinated
    m = ( (df_p['nr_covid_vax'].notnull()==True) )
    df_p.loc[m, "vaccinated_bit"] = 1
    df_p.loc[m, "week_nr_firstvax"] = df_p.loc[m, "covid_vax_firstdate"].dt.isocalendar().week
    df_p.loc[m, "year_firstvax"] = df_p.loc[m, "covid_vax_firstdate"].dt.isocalendar().year

    # All unvaccinated
    m = ( (df_p['nr_covid_vax'].notnull()==False) )
    df_p.loc[m, "vaccinated_bit"] = 0

    # "DEELSCOREWELVAART","DEELSCOREOPLEIDINGSNIVEAU_1","DEELSCORERECENTARBEIDSVERLEDEN","TOTAALSCORE_1"
    # All missing SESWOA people: set vals to 0
    print("Set missing SESWOA info")
    m = ( (df_p['DEELSCOREWELVAART'].notnull()==False) )
    df_p.loc[m, "DEELSCOREWELVAART"] = 0
    df_p.loc[m, "DEELSCOREOPLEIDINGSNIVEAU_1"] = 0
    df_p.loc[m, "DEELSCORERECENTARBEIDSVERLEDEN"] = 0
    df_p.loc[m, "TOTAALSCORE_1"] = 0

    print("bin calc: GBAGEBOORTEJAAR")
    birthyear_to = 1930
    m = ( (df_p["GBAGEBOORTEJAAR"]<birthyear_to) )
    df_p.loc[m, "GBAGEBOORTEJAAR_bin"] = 0
    stepsize = 5
    binnr = 1
    for birthyear in range(1930,2016,stepsize):
        birthyear_from = birthyear
        birthyear_to = birthyear_from + stepsize
        print(birthyear_from)
        m = ( (df_p["GBAGEBOORTEJAAR"]>=birthyear_from) & (df_p["GBAGEBOORTEJAAR"]<birthyear_to) )
        df_p.loc[m, "GBAGEBOORTEJAAR_bin"] = binnr
        binnr += 1

    birthyear_from = 2020
    m = ( (df_p["GBAGEBOORTEJAAR"]>=birthyear_from) )
    df_p.loc[m, "GBAGEBOORTEJAAR_bin"] = binnr

    # med_rxrisk_score bins:
    print("bin calc: med_rxrisk_score_simplesum_prevyear")
    m = ( (df_p["med_rxrisk_score_simplesum_prevyear"]<=0) )
    df_p.loc[m, "med_rxrisk_score_simplesum_prevyear_bin"] = 0
    m = ( (df_p["med_rxrisk_score_simplesum_prevyear"]>0) & (df_p["med_rxrisk_score_simplesum_prevyear"]<=5) )
    df_p.loc[m, "med_rxrisk_score_simplesum_prevyear_bin"] = 1
    m = ( (df_p["med_rxrisk_score_simplesum_prevyear"]>5) & (df_p["med_rxrisk_score_simplesum_prevyear"]<=10) )
    df_p.loc[m, "med_rxrisk_score_simplesum_prevyear_bin"] = 2
    m = ( (df_p["med_rxrisk_score_simplesum_prevyear"]>10) & (df_p["med_rxrisk_score_simplesum_prevyear"]<=15) )
    df_p.loc[m, "med_rxrisk_score_simplesum_prevyear_bin"] = 3
    m = ( (df_p["med_rxrisk_score_simplesum_prevyear"]>15) & (df_p["med_rxrisk_score_simplesum_prevyear"]<=20) )
    df_p.loc[m, "med_rxrisk_score_simplesum_prevyear_bin"] = 4
    m = ( (df_p["med_rxrisk_score_simplesum_prevyear"]>20) )
    df_p.loc[m, "med_rxrisk_score_simplesum_prevyear_bin"] = 5
    
    print("bin calc: med_rxrisk_score_weightedpratt_prevyear")
    m = ( (df_p["med_rxrisk_score_weightedpratt_prevyear"]<=0) )
    df_p.loc[m, "med_rxrisk_score_weightedpratt_prevyear_bin"] = 0
    m = ( (df_p["med_rxrisk_score_weightedpratt_prevyear"]>0) & (df_p["med_rxrisk_score_weightedpratt_prevyear"]<=5) )
    df_p.loc[m, "med_rxrisk_score_weightedpratt_prevyear_bin"] = 1
    m = ( (df_p["med_rxrisk_score_weightedpratt_prevyear"]>5) & (df_p["med_rxrisk_score_weightedpratt_prevyear"]<=10) )
    df_p.loc[m, "med_rxrisk_score_weightedpratt_prevyear_bin"] = 2
    m = ( (df_p["med_rxrisk_score_weightedpratt_prevyear"]>10) & (df_p["med_rxrisk_score_weightedpratt_prevyear"]<=15) )
    df_p.loc[m, "med_rxrisk_score_weightedpratt_prevyear_bin"] = 3
    m = ( (df_p["med_rxrisk_score_weightedpratt_prevyear"]>15) & (df_p["med_rxrisk_score_weightedpratt_prevyear"]<=20) )
    df_p.loc[m, "med_rxrisk_score_weightedpratt_prevyear_bin"] = 4
    m = ( (df_p["med_rxrisk_score_weightedpratt_prevyear"]>20) )
    df_p.loc[m, "med_rxrisk_score_weightedpratt_prevyear_bin"] = 5
    # print(df_p.shape)

    print()

    # versionstr = "_v0B"
    filename_core = "GBAPERSOON_trackable_2018_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins" + versionstr

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_p.head(1000).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_p.to_feather(filename_ftr)
    print(time.time() - start)



if __name__ == '__main__':
    run_main()


    