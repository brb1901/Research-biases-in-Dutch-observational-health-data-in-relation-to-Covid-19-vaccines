import os
import pandas as pd
import time
import argparse
from lifelines import KaplanMeierFitter
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
  
    # nr_dead = len(df_in_dead)
    # prop_dead = float(nr_dead)/float(nr_people)
    # print("nr_people: " + str(nr_people) + " nr_dead: " + str(nr_dead))
    # print("prop_dead: " + str(prop_dead))

    # mean_time_to_death = df_in_dead["time_to_death"].mean()
    # print("mean_time_to_death: " + str(mean_time_to_death))
    # print()

    # max_time_to_death = 2000 #df_in_dead["time_to_death"].max()
    kmf = KaplanMeierFitter()
    kmf.fit(durations = df_p["time_to_death"], event_observed = df_p["dead"], label=labeltext)
    # kmf.event_table

    # kmf.predict(range(0,int(max_time_to_death)-250)) # +1
    print("Prop. alive after 1 year:")
    surv_propval = kmf.predict(365)
    print(surv_propval)
    dead_propval = 1-surv_propval

    # kmf.median_survival_time_
    # kmf.plot()
    # plt.title("Kaplan-Meier Survival Curve")
    # plt.ylabel("Probability of survival")
    # plt.show()
    return [kmf, max_time_to_death, dead_propval]



def run_main(birthyear_from_str, birthyear_to_str, wlz_bit_str, med_rxrisk_scores_str):
    basepath = "H:/data/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    # basepath_csv_matched = basepath+"csv/matched/"

    versionstr = "_v3"

    filename_core_prefix = "matchedset_trackable_2021_"

    birthyear_from_total = int(birthyear_from_str)
    birthyear_to_total = int(birthyear_to_str)
    wlz_bit = int(wlz_bit_str)
    med_rxrisk_scores = int(med_rxrisk_scores_str)

    filename_core = filename_core_prefix + str(birthyear_from_total) + "_" + str(birthyear_to_total) + "_WLZ" + str(wlz_bit) + versionstr

    filename_ftr = basepath_ftr_matched+filename_core+".ftr"
    print("reading: " + filename_core)
    df_p = pd.read_feather(filename_ftr)
    print(df_p.shape)

    if med_rxrisk_scores==0:
        print("HEALTHY SUBGROUP: df_p = df_p[ (df_p'med_rxrisk_score_weightedpratt_prevyear_bin']==0) ]")
        df_p = df_p[ (df_p["med_rxrisk_score_weightedpratt_prevyear_bin"]<=0) ]
    elif med_rxrisk_scores==1:
        print("UNHEALTHY SUBGROUP: df_p = df_p[ (df_p'med_rxrisk_score_weightedpratt_prevyear_bin']>0) ]")
        df_p = df_p[ (df_p["med_rxrisk_score_weightedpratt_prevyear_bin"]>0) ]

    # df_p["start_weeknr"] = df_p["start_date"].dt.isocalendar().week

    for i in [0,1,2]:  #,1,2
        mortalitytype = i

        for vax in [0,1]: # ,2
            [kmf, max_time_to_death, dead_propval] = analyze(df_p, mortalitytype, vax)
            kmf.plot(ci_show=True, loc=slice(0,max_time_to_death-0))  # max_time_to_death-250
            # print(kmf.survival_function_.head())  
            filename_csv = "H:/data/output/csv_python/ves/surv_curves/surv_curve_vax" + str(vax) + "_morttype" +str(mortalitytype) +"_" + str(birthyear_from_total) +"-" + str(birthyear_to_total) +"_WLZbit" + str(wlz_bit)+"_RxRisk" +str(med_rxrisk_scores) + versionstr 
            print("writing: "+filename_csv+ ".csv")
            kmf.survival_function_.to_csv(filename_csv + ".csv")
            if vax==1:
                var = dead_propval
            elif vax==0:
                nvar = dead_propval 
            # kmf.survival_function_.plot()
        print("NVAR: " + str(nvar) + ", VAR: " + str(var))
        VE_RRR = (nvar-var)/nvar
        print("VE (RRR): " + str(VE_RRR))
        VE_ARR = (nvar-var)
        print("VE (ARR): " + str(VE_ARR))
        print()
        plt.title("Kaplan-Meier Survival Curve, " + str(birthyear_from_total) + "-" + str(birthyear_to_total) + ", WLZ " + str(wlz_bit)+ ", RxRisk " + str(med_rxrisk_scores) + ", " + versionstr)
        plt.ylabel("probability of survival")
        plt.xlabel("time since treatment (days)")
        filename_fig = "H:/data/output/plots/ves/surv_curves/surv_curves_morttype" +str(mortalitytype) +"_" + str(birthyear_from_total) +"-" + str(birthyear_to_total) +"_WLZbit" + str(wlz_bit) +"_RxRisk" +str(med_rxrisk_scores) + versionstr 
        plt.savefig(filename_fig + ".pdf", format="pdf", bbox_inches="tight")
        plt.show()   


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("birthyear_from_str")
    parser.add_argument("birthyear_to_str")
    parser.add_argument("wlz_bit_str")
    parser.add_argument("med_rxrisk_scores_str")
    args = parser.parse_args()
    run_main(args.birthyear_from_str, args.birthyear_to_str, args.wlz_bit_str, args.med_rxrisk_scores_str)
    