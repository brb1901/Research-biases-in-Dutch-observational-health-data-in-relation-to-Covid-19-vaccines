import pandas as pd
# import argparse
# from generic_functions_calc_deaths_perperiod import calc_deaths_per_period
import os

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

def calc_mode_perc(df_p, val_interest_str, nr_people):
    print(val_interest_str)
    val = df_p[val_interest_str].mode()[0]
    print("Mode: "+ str(val))
    df_p_test = df_p[(df_p[val_interest_str]==val) ]
    nr_p = len( df_p_test )
    print("Number of people with this value: " + str(nr_p))
    print("Percentage of people with this value: " + str(100.0*float(nr_p)/float(nr_people)))


def run_main():
    basepath = "H:/data/"
    basepath_ftr_unmatched = basepath+"python_pandas/matched/"
    # basepath_csv_unmatched = basepath+"csv/unmatched/"

    filename_core_prefix = "matchedset_trackable_2021_" + "extra1_"
    # mat_str = "matched"
    # weeksteps = 4
    stepsize = 10
    versionstr = "_v3"

    # out_versionstr = versionstr+"E"

    # for birthyear in range(2010,1909,-stepsize):
    print()
    # for birthyear in range(1920,2001,stepsize):
    for wlz_bit in [1]: # [0,1]:
        print("WLZ " + str(wlz_bit))
        print()
        for birthyear in [1930,1940,1950,1960,1980,2000]: # 1930,1940,1950,1960,1980,2000

            birthyear_from = birthyear
            birthyear_to = birthyear_from + stepsize
            # age_from = refyear - birthyear_to
            # age_to = refyear - birthyear_from
            print(birthyear_from)
            print(birthyear_to)
            print()

            ok_bit = True
            if birthyear_from>=1960 and birthyear_from<2000: # ==2000
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
                    df_ps = pd.concat([df_p1,df_p2], ignore_index=True)
                    df_ps.reset_index(inplace=True,drop=True)
                    birthyear_to = birthyear_from+20
                    print("20 YEARS SUCCESS")

            elif birthyear_from==2000:
                print("20 YEARS")
                # birthyear_from_temp = birthyear_from
                birthyear_to = birthyear_from + 20
                filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr
                filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
                if os.path.exists(filename_ftr):
                    print("reading: " + filename_core)
                    df_ps = pd.read_feather(filename_ftr)     
                else:
                    ok_bit = False
            else:
                filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr
                filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
                if os.path.exists(filename_ftr):
                    print("reading: " + filename_core)
                    df_ps = pd.read_feather(filename_ftr)     
                else:
                    ok_bit = False

            # if birthyear_from>=1960:
            #     weeksteps = 13
            # else:
            #     weeksteps = 4

            # med_rxrisk_scores = -1
            # wlz_levels = -1

            if ok_bit:  
                refyear = 2021
                df_ps["GBAGEBOORTEJAAR"]=  df_ps["GBAGEBOORTEJAAR"].astype('int')
                df_ps["leeftijd_in_ditjaar"] = refyear - df_ps["GBAGEBOORTEJAAR"]
                df_ps["GBAGESLACHT"]=  df_ps["GBAGESLACHT"].astype('int')

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

                    val_interest_str = "leeftijd_in_ditjaar"
                    calc_mean_stddev(df_p, val_interest_str)
                    
                    val_interest_str = "GBAGESLACHT"
                    val=1 # man
                    calc_perc(df_p, val_interest_str, val, nr_people)
                    # val=2 # vrouw
                    # calc_perc(df_p, val_interest_str, val, nr_people)

                    # val_interest_str = "WLZ_bit"
                    # # val=0 # geen WLZ
                    # # calc_perc(df_p, val_interest_str, val, nr_people)
                    # val=1 # wel WLZ
                    # calc_perc(df_p, val_interest_str, val, nr_people)

                    # med_rxrisk_score_weightedpratt_prevyear
                    val_interest_str = "med_rxrisk_score_weightedpratt_prevyear"
                    calc_mean_stddev(df_p, val_interest_str)

                    if wlz_bit:
                        val_interest_str = "WLZ_type"
                        # calc_mean_stddev(df_p, val_interest_str)
                        calc_mode_perc(df_p, val_interest_str, nr_people)
                        val_interest_str = "WLZ_level"
                        calc_mean_stddev(df_p, val_interest_str)
                

            else:
                print("file does not exist, skipping this subgroup")

            print()
            input("Press enter to continue")
            print()
    

if __name__ == '__main__':
    run_main()
    


 