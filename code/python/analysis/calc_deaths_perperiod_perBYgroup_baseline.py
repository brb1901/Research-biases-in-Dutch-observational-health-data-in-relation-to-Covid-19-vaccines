import pandas as pd
# import argparse
from generic_functions_calc_deaths_perperiod import calc_deaths_per_period
import math
from datetime import date, datetime, timedelta

def calc_deaths_per_period_baseline(df_ps, age_from, age_to, weeksteps):
    # year = 2016 # 2019 # 2018 2021 # 
    # year_tostop = 2020 #2022 #  
    # nr_years_data = 4 # year_tostop - year
    # nr_years_predict = 3 

    # # age_from = refyear - birthyear_to
    # # birthyear_to = refyear - age_from
    # # age_to = refyear - birthyear_from
    # # birthyear_from = refyear - age_to
    # # 
    # yearsstr = "2016-2019" # "2021" #"2019-2022" # 
    # year_prev = year - 1
    # year_first = year
    
    # print("First year:")
    # print(year)

    df_out = None
    for i_year_predict in range(3): # 0,1,2
        print(i_year_predict)
        age_from_thisyear = age_from + i_year_predict
        age_to_thisyear = age_to + i_year_predict
        print(age_from_thisyear)
        print(age_to_thisyear)
        
        for year_data in [2016, 2017, 2018, 2019]:
            print(year_data)
            birthyear_to = year_data - age_from_thisyear
            birthyear_from = year_data - age_to_thisyear

            df_p = df_ps[ (df_ps['GBAGEBOORTEJAAR']>=birthyear_from) & (df_ps['GBAGEBOORTEJAAR']<birthyear_to) & 
                          ((df_ps["dead_bit"]==0) | (df_ps["year_dead"] >= year_data)) ] 
            nr_p_ag = len( df_p )
            print("Number of people in this age group (alive) at start of processing: " + str(nr_p_ag))
            # df_p_test = df_p[ (df_p['year_dead']==year_data)  ]
            # print("Number of people in this age group who died this year : " + str(len(df_p_test))) 

            df_temp = None
            nr_years_withdata = 0
            if nr_p_ag==0:
                print("Number of people alive and present in this age group is zero! Ending this analysis for this group")
            else:
                nr_years_withdata += 1
                df_temp = pd.DataFrame()
                if df_out is None:
                    df_out = pd.DataFrame()
                week_nr_thisyear_list = [] #[int(0)] * 52/weeksteps
                # nr_deaths_list = [] 
                # nr_peoplealive_list = []
                perc_deaths_list = []
                date_from = date(year_data,1,1)
                # date_to = date_from + timedelta(weeks = weeksteps)
                # weeknr = 0 + weeksteps
                week_nr_thisyear = 0 + weeksteps # date_to.isocalendar().week
                year_from = date_from.isocalendar().year

                while year_from==year_data:
                    week_nr_thisyear_list.append(week_nr_thisyear)

                    # Who died in this period?
                    df_pd = df_p[ (df_p["year_dead"] == year_data) & ((df_p["week_nr_dead"] <= week_nr_thisyear) & 
                                        (df_p["week_nr_dead"] > (week_nr_thisyear-weeksteps))) ]
                    nr_deaths_all = len(df_pd)
                    # nr_deaths_list.append(nr_deaths_all)
                    # nr_peoplealive_list.append(nr_p_ag)
                    perc_deaths_list.append( float(nr_deaths_all)/float(nr_p_ag) * 100.0 )
                    # nr_deaths_total += nr_deaths_all
                    # weeknr += weeksteps
                    date_from = date_from + timedelta(weeks = weeksteps)
                    # date_to = date_from + timedelta(weeks = weeksteps)
                    week_nr_thisyear += weeksteps # = date_to.isocalendar().week
                    year_from = date_from.isocalendar().year
                    nr_p_ag -= nr_deaths_all

                df_temp[str(year_data)] = perc_deaths_list # nr_deaths_list

        if nr_years_withdata>0:
            print("filling df_out with data")
            df_temp["mean"] = df_temp.mean(axis=1)
            df_temp["week_nr_thisyear"] = week_nr_thisyear_list
            if i_year_predict==0:
                df_out["week_nr_thisyear"] = week_nr_thisyear_list
            df_out[str(i_year_predict)] = df_temp["mean"]

    print()
    return df_out

def run_main():
    basepath = "H:/data/"

    weeksteps =  13 # 4 # 13 #
    versionstr = "_v0"
    refyear = 2021

    filename_core = "GBAPERSOON_trackable_years2016-2020_DeadInfo" + versionstr
    print("reading: " + filename_core)
    df_ps = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")

    print("adding some extra analysis data..")
    df_ps["week_nr_dead"] = -1
    df_ps["year_dead"] = -1

    df_ps["dead_date"] = pd.to_datetime(df_ps["dead_date"])
    m = ( (df_ps["dead_bit"]==1) )
    df_ps.loc[m, "week_nr_dead"] = df_ps.loc[m, "dead_date"].dt.isocalendar().week
    df_ps.loc[m, "year_dead"] = df_ps.loc[m, "dead_date"].dt.isocalendar().year

    stepsize = 10 # 20 # 10 # 

    for birthyear in range(1920,2001,stepsize): # 1910,2011 # 2000,2001
    # stepsize = 100
    # for birthyear in range(1910,2009,stepsize):
        birthyear_from = birthyear
        # if birthyear_from==2000:
        #      birthyear_to = birthyear_from + 20
        # else:
        #     birthyear_to = birthyear_from + stepsize
        birthyear_to = birthyear_from + stepsize
        age_from = refyear - birthyear_to
        age_to = refyear - birthyear_from
        print(birthyear_from)
        print(birthyear_to)
        print(age_from)
        print(age_to)
        print()
    
        df_out = calc_deaths_per_period_baseline(df_ps, age_from, age_to, weeksteps) # , refyear
        if df_out is not None:
            # deaths_baselines
            filename_core = "deaths_baseline_" + str(age_from) + "_" + str(age_to) + "_" + str(weeksteps) + versionstr

            filename_csv = basepath+"csv/deaths_baselines/" +filename_core+".csv"
            print("writing: "+filename_csv)
            df_out.to_csv(filename_csv)

            filename_ftr = basepath+"python_pandas/deaths_baselines/"+filename_core+".ftr"
            print("writing: "+filename_ftr)
            df_out.to_feather(filename_ftr)
    
    

if __name__ == '__main__':
    run_main()
    


 