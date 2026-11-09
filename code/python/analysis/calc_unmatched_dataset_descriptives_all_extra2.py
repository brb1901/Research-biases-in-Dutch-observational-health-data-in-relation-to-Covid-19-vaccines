import pandas as pd
# import argparse
# from generic_functions_calc_deaths_perperiod import calc_deaths_per_period
import time

def calc_mean_stddev(df_p, val_interest_str):
    print(val_interest_str)                
    mean_val = df_p[val_interest_str].mean()
    print("mean_val: " + str(mean_val))
    stddev = df_p[val_interest_str].std()
    print("stddev: " + str(stddev))

def calc_perc(df_p, val_interest_str, val, nr_people):
    print(val_interest_str)
    print(val)
    df_p_test = df_p[(df_p[val_interest_str]==val) ]
    nr_p = len( df_p_test )
    print("Number of people with this value: " + str(nr_p))
    print("Percentage of people with this value: " + str(100.0*float(nr_p)/float(nr_people)))


def run_main():
    basepath = "H:/data/"
    # basepath_ftr = basepath+"python_pandas/GBA/"
    # basepath_csv = basepath+"csv/GBA/"
    # basepath_ftr_unmatched = basepath+"python_pandas/unmatched/"
    # basepath_csv_unmatched = basepath+"csv/unmatched/"

    versionstr = "_v0"
    refyear = 2021

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead" + versionstr
    print("reading: " + filename_core)
    df_ps = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")

    print("adding some extra analysis data..")
    df_ps["treatment"] = 0
    df_ps["control"] = 0
    # df_p["week_nr_dead"] = -1
    # df_p["year_dead"] = -1

    m = ( (df_ps["vaccinated_bit"]==1) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
    df_ps.loc[m, "treatment"] = 1
    m = ( (df_ps["vaccinated_bit"]==0) ) # dit is nu obv PRIK 1; en geen 2/3 weken delay of zo
    df_ps.loc[m, "control"] = 1

    print("computing and adding leeftijd_in_ditjaar")
    start = time.time()
    df_ps["GBAGEBOORTEJAAR"]=  df_ps["GBAGEBOORTEJAAR"].astype('int')
    df_ps["leeftijd_in_ditjaar"] = refyear - df_ps["GBAGEBOORTEJAAR"]
    print(time.time() - start)

    df_ps["GBAGESLACHT"]=  df_ps["GBAGESLACHT"].astype('int')

    df_ps = df_ps[ (df_ps['GBAGEBOORTEJAAR']>=1930) & (df_ps['GBAGEBOORTEJAAR']<2020)]

    NLCODE = int(6030)
    df_ps["GBAGEBOORTELAND"]=  df_ps["GBAGEBOORTELAND"].astype('int')
    df_ps["GBAGEBOORTELANDMOEDER"]=  df_ps["GBAGEBOORTELANDMOEDER"].astype('int')
    df_ps["GBAGEBOORTELANDVADER"]=  df_ps["GBAGEBOORTELANDVADER"].astype('int')
    df_ps["born_NL_parents_too"] = 0
    df_ps["born_NL_atleast1parent_not"] = 0
    df_ps["born_NL_not"] = 0
    # m = ( (df_cp["year"]==2019) | ((df_cp["year"]==2020) & (df_cp["yearweeknr"]<10)) )
    m = ( (df_ps["GBAGEBOORTELAND"]==NLCODE) & (df_ps["GBAGEBOORTELANDMOEDER"]==NLCODE) & (df_ps["GBAGEBOORTELANDVADER"]==NLCODE) ) 
    df_ps.loc[m, "born_NL_parents_too"] = 1
    m = ( (df_ps["GBAGEBOORTELAND"]==NLCODE) & ((df_ps["GBAGEBOORTELANDMOEDER"]!=NLCODE) | (df_ps["GBAGEBOORTELANDVADER"]!=NLCODE)) ) 
    df_ps.loc[m, "born_NL_atleast1parent_not"] = 1
    m = ( (df_ps["GBAGEBOORTELAND"]!=NLCODE) ) 
    df_ps.loc[m, "born_NL_not"] = 1

    # born_abroad = 0
    # born_atleast1parent_abroad = 0
    # GBAGEBOORTELAND = int(rowdata["GBAGEBOORTELAND"])
    # GBAGEBOORTELANDMOEDER = int(rowdata["GBAGEBOORTELANDMOEDER"])
    # GBAGEBOORTELANDVADER = int(rowdata["GBAGEBOORTELANDVADER"])
    
    # #DEBUG
    # # print(GBAGEBOORTELAND)
    # if GBAGEBOORTELAND != NLCODE:
    #     born_abroad = 1
    # if (GBAGEBOORTELANDMOEDER != NLCODE) or (GBAGEBOORTELANDVADER != NLCODE):
    #     born_atleast1parent_abroad = 1

    stepsize10 = 10
    stepsize20 = 20
    # print()

    nr_people_all = len(df_ps)
    print(nr_people_all)
    print()

    for treatment in [1,0]:
        print()
        if treatment:
            print("VACCINATED")
        else:
            print("UNVACCINATED")
        print()
        df_p = df_ps[ (df_ps['treatment']==treatment)]
        nr_people = len(df_p)
        print(nr_people)
        print("Percentage of people with this status: " + str(100.0*float(nr_people)/float(nr_people_all)))
        print()

        # val_interest_str = "leeftijd_in_ditjaar"
        # calc_mean_stddev(df_p, val_interest_str)
        
        # val_interest_str = "GBAGESLACHT"
        # val=1 # man
        # calc_perc(df_p, val_interest_str, val, nr_people)
        # # val=2 # vrouw
        # # calc_perc(df_p, val_interest_str, val, nr_people)

        # val_interest_str = "WLZ_bit"
        # # val=0 # geen WLZ
        # # calc_perc(df_p, val_interest_str, val, nr_people)
        # val=1 # wel WLZ
        # calc_perc(df_p, val_interest_str, val, nr_people)

        # # med_rxrisk_score_weightedpratt_prevyear
        # val_interest_str = "med_rxrisk_score_weightedpratt_prevyear"
        # calc_mean_stddev(df_p, val_interest_str)

        # val_interest_str = "dead_bit"
        # val=1 
        # calc_perc(df_p, val_interest_str, val, nr_people)

        # val_interest_str = "dead_bit_covid"
        # val=1 
        # calc_perc(df_p, val_interest_str, val, nr_people)

        # val_interest_str = "dead_bit_noncovid"
        # val=1 
        # calc_perc(df_p, val_interest_str, val, nr_people)

        val_interest_str = "born_NL_parents_too"
        val=1 
        calc_perc(df_p, val_interest_str, val, nr_people)

        val_interest_str = "born_NL_atleast1parent_not"
        val=1 
        calc_perc(df_p, val_interest_str, val, nr_people)

        val_interest_str = "born_NL_not"
        val=1 
        calc_perc(df_p, val_interest_str, val, nr_people)

        val_interest_str = "DEELSCOREWELVAART"
        calc_mean_stddev(df_p, val_interest_str)
        val_interest_str = "DEELSCOREOPLEIDINGSNIVEAU_1"
        calc_mean_stddev(df_p, val_interest_str)
        val_interest_str = "DEELSCORERECENTARBEIDSVERLEDEN"
        calc_mean_stddev(df_p, val_interest_str)
          

        # for birthyear in [1930,1940,1950,1960,1980,2000]: # 1930,1940,1950,1960,1980,2000
        #     if birthyear>=1960:
        #         stepsize = stepsize20
        #     else:
        #         stepsize = stepsize10

        #     birthyear_from = birthyear
        #     birthyear_to = birthyear_from + stepsize
        #     print(birthyear_from)
        #     print(birthyear_to)
        #     print()

        #     df_p = df_ps[ (df_ps['GBAGEBOORTEJAAR']>=birthyear_from) & (df_ps['GBAGEBOORTEJAAR']<birthyear_to) & (df_ps['treatment']==treatment)]
        #     nr_p = len(df_p)
        #     print(nr_p)
        #     print("Percentage of people in this age cohort: " + str(100.0*float(nr_p)/float(nr_people)))
        #     print()


if __name__ == '__main__':
    run_main()
    


 