import pandas as pd
# import argparse
# from generic_functions_calc_deaths_perperiod import calc_deaths_per_period


def run_main():
    basepath = "H:/data/"
    # basepath_ftr = basepath+"python_pandas/GBA/"
    # basepath_csv = basepath+"csv/GBA/"
    basepath_ftr_unmatched = basepath+"python_pandas/unmatched/"
    basepath_csv_unmatched = basepath+"csv/unmatched/"

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

    filename_core_prefix = "unmatchedset_trackable_2021_"

    stepsize = 10
    for birthyear in range(2010,1909,-stepsize):
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
            df_p = df_ps[ (df_ps['GBAGEBOORTEJAAR']>=birthyear_from) & (df_ps['GBAGEBOORTEJAAR']<birthyear_to) & 
                        (df_ps['WLZ_bit']==wlz_bit) ]
            nr_people = len(df_p)
            print(nr_people)
            
            if nr_people:
                df_p.reset_index(inplace=True,drop=True)
                filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr

                filename_csv = basepath_csv_unmatched+filename_core+"_head.csv"
                print("writing (head): "+filename_csv)
                df_p.head(1000).to_csv(filename_csv)

                filename_ftr = basepath_ftr_unmatched+filename_core+".ftr"
                print("writing: "+filename_ftr)
                df_p.to_feather(filename_ftr)
            else:
                print("empty, skipping this subgroup")

        print()


if __name__ == '__main__':
    run_main()
    


 