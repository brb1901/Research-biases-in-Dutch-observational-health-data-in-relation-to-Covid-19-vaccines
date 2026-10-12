import pandas as pd
import time
# from datetime import date
# import gc
# import math
# import os
import argparse

def run_main(yearstring):
    basepath = "H:/data/"
    # basepath_ftr_seswoa = basepath+"python_pandas/SESWOA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"
    # basepath_ftr_medicijn = basepath+"python_pandas/MEDICIJN/"

    versionstr = "_v0"
    # refyear = 2021

    filename_core = "GBAPERSOON_trackable_2018and2021" # + versionstr
    print("reading: " + filename_core)
    df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_p.shape)

    # df_indiv["covid_pos_test"] = 0
    # df_indiv["covid_pos_test_date"] = None 

    year = int(yearstring)

    # for year in [2020,2021]:
    yearstr = str(year)

    df_p["covidinf_"+yearstr+"_"+"week1nr"] = -1
    df_p["covidinf_"+yearstr+"_"+"week2nr"] = -1
    df_p["covidinf_"+yearstr+"_"+"week3nr"] = -1
    df_p["covidinf_"+yearstr+"_"+"week4nr"] = -1
    df_p["covidinf_"+yearstr+"_"+"date1"] = None
    df_p["covidinf_"+yearstr+"_"+"date2"] = None
    df_p["covidinf_"+yearstr+"_"+"date3"] = None
    df_p["covidinf_"+yearstr+"_"+"date4"] = None
        
    df_p["handled"] = 0

    print("processing...")

    start_overall = time.time()
    start = time.time()
    total_nr_infections = 0
    # for year in [2020,2021]:
    #     yearstr = str(year)

    filename_cov = basepath+"python_pandas/GGDCOVID19/"+"HPZonedata_" + yearstr + ".ftr"
    print("reading "+ filename_cov)
    df_covid_year = pd.read_feather(filename_cov)
    df_covid_year["datetimeobj"] = pd.to_datetime(df_covid_year["TijdstiprapportageCOVID19besmetting"], errors = 'coerce')
    if year==2021:
        df_covid_year["RINPERSOON"] = df_covid_year["Rinpersoon"]

    for index, rowdata in df_p.iterrows():
        if index % 1000 == 0:
            print(index)
            # print(rowdata)      
            print(total_nr_infections)
            print(time.time() - start)
            start = time.time()
            print()
            if index % 100000 == 0:
                filename_core = "GBAPERSOON_trackable_2018and2021_covidinf_temp_"+ yearstr + versionstr

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

        rinp_str = rowdata["RINPERSOON"]
        # rows=None
        rows = df_covid_year.loc[ (df_covid_year["RINPERSOON"] == rinp_str) ]
        nr_rows = len(rows)
        nr_pos = 0
        prev_weeknr = -1
        for j in range(nr_rows):
            # print("covid")
            # TypeuitslagCOVID19test
            result = int(rows.iloc[j]["TypeuitslagCOVID19test"])
            if result>=1 and result<=3: # positief
                nr_pos += 1
                this_date = rows.iloc[j]["datetimeobj"]
                weeknr = this_date.isocalendar()[1]
                month = this_date.month
                if month == 12 and (weeknr==1 or weeknr==53):
                    weeknr=52
                    
                if nr_pos==1:
                    df_p.at[index, "covidinf_"+yearstr+"_"+"week1nr"] = weeknr
                    df_p.at[index, "covidinf_"+yearstr+"_"+"date1"] = this_date       
                    total_nr_infections+=1                 
                elif nr_pos==2:
                    if weeknr != prev_weeknr:
                        df_p.at[index, "covidinf_"+yearstr+"_"+"week2nr"] = weeknr
                        df_p.at[index, "covidinf_"+yearstr+"_"+"date2"] = this_date
                        total_nr_infections+=1
                elif nr_pos==3:
                    if weeknr != prev_weeknr:
                        df_p.at[index, "covidinf_"+yearstr+"_"+"week3nr"] = weeknr
                        df_p.at[index, "covidinf_"+yearstr+"_"+"date3"] = this_date
                        total_nr_infections+=1
                else: # so all positive tests >= the fourth will be marked as the fourth!
                    if weeknr != prev_weeknr:
                        df_p.at[index, "covidinf_"+yearstr+"_"+"week4nr"] = weeknr
                        df_p.at[index, "covidinf_"+yearstr+"_"+"date4"] = this_date
                        total_nr_infections+=1
                prev_weeknr = weeknr

        df_p.at[index, "handled"]=1
        #DEBUG
        # if index>1001:
        #     break


    print(df_p.shape)
    print("total_nr_infections:")
    print(total_nr_infections)

    # df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    # df_p.reset_index(inplace=True,drop=True)

    # print()
    # print("Number of dead")
    # print(nr_dead)   
    print("Overall processing time:")
    print(time.time() - start_overall)
    print()

    filename_core = "GBAPERSOON_trackable_2018and2021_covidinf_" + yearstr + versionstr

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
    parser = argparse.ArgumentParser()
    parser.add_argument("yearstring")
    args = parser.parse_args()
    run_main(args.yearstring)


    