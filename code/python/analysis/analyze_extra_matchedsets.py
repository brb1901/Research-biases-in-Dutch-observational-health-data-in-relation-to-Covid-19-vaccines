import os
import pandas as pd
import time
import argparse
# from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import numpy as np


def analyze(df_p, mortalitytype, treatment):
    df_p = df_p.copy()
    print("mortalitytype: " + str(mortalitytype) )

    # if treatment == 1:
    if treatment == 0 or treatment == 1:
        df_p = df_p[ (df_p['treatment']==treatment) ] # & (df_p['acute_ZA']==acute_ZA)
    # else: ALL!

    if mortalitytype == 0:
        labeltext = "ACM"
        df_p["dead"] = df_p["dead_bit"]
    elif mortalitytype == 1:
        labeltext = "Covid"
        df_p["dead"] = df_p["dead_bit_covid"]
    elif mortalitytype == 2:
        labeltext = "Non-Covid"
        df_p["dead"] = df_p["dead_bit_noncovid"]
    if treatment==1:
        labeltext += " Vaccinated"
    elif treatment==0:
        labeltext += " Unvaccinated"
    else:
        labeltext += " All"
    print(labeltext)

    nr_people = len(df_p)
    print(nr_people)

    # df_in["time_to_death"] = df_in["dead"].astype(float)
    df_p["time_to_death"] = 3000 # float("NaN")

    max_time_to_death = -9
    for index, rowdata in df_p.iterrows():
        if rowdata["dead"]==1:
            # if rowdata["dead_date"].year<2022:
            time_to_death = (rowdata["dead_date"] - rowdata["start_date"]).days
            df_p.at[index,"time_to_death"]=float(time_to_death)
            if time_to_death>max_time_to_death:
                max_time_to_death=time_to_death


    for index, rowdata in df_p.iterrows():
        if rowdata["dead"]==0:
            df_p.at[index,"time_to_death"]=float(max_time_to_death)

    plt.hist(df_p["start_weeknr"])
    plt.title("Histogram of this group, dead or alive, " + labeltext)
    plt.ylabel("number of cases")
    plt.xlabel("start_weeknr")
    plt.show()

    df_p = df_p[ (df_p["time_to_death"]<=30) ]

    nr_dead = len(df_p)
    print("nr_dead: " + str(nr_dead))

    plt.hist(df_p["start_weeknr"])
    plt.title("Histogram of dead in first 30 days after start-date, " + labeltext)
    plt.ylabel("number of cases")
    plt.xlabel("start_weeknr")
    plt.show()


    # prop_dead = float(nr_dead)/float(nr_people)
    # print("nr_people: " + str(nr_people) + " nr_dead: " + str(nr_dead))
    # print("prop_dead: " + str(prop_dead))

    # mean_time_to_death = df_in_dead["time_to_death"].mean()
    # print("mean_time_to_death: " + str(mean_time_to_death))
    # print()




def run_main(birthyear_from_str, birthyear_to_str, wlz_bit_str):
    basepath = "H:/data/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    basepath_csv_matched = basepath+"csv/matched/"

    versionstr = "_v3"

    filename_core_prefix = "matchedset_trackable_2021_"

    birthyear_from_total = int(birthyear_from_str)
    birthyear_to_total = int(birthyear_to_str)
    wlz_bit = int(wlz_bit_str)

    filename_core = filename_core_prefix + str(birthyear_from_total) + "_" + str(birthyear_to_total) + "_WLZ" + str(wlz_bit) + versionstr

    filename_ftr = basepath_ftr_matched+filename_core+".ftr"
    print("reading: " + filename_core)
    df_p = pd.read_feather(filename_ftr)
    print(df_p.shape)

    df_p["start_weeknr"] = df_p["start_date"].dt.isocalendar().week

    for i in [0,1,2]:  #,1,2
        mortalitytype = i

        for vax in [0,1]: # ,2
            analyze(df_p, mortalitytype, vax)
    

    # versionstr = "_v7b"
    # plt.savefig("H:/data/output/plots/surv_curves" + versionstr + ".pdf", format="pdf", bbox_inches="tight")



    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("birthyear_from_str")
    parser.add_argument("birthyear_to_str")
    parser.add_argument("wlz_bit_str")
    args = parser.parse_args()
    run_main(args.birthyear_from_str, args.birthyear_to_str, args.wlz_bit_str)
    