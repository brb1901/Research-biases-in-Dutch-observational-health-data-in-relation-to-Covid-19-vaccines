import pandas as pd
# import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from generic_functions import read_population_NL_all, read_population_NL_men, read_population_NL_women, get_nr_people_fromto_age
import numpy as np


def run_main():
    basepath = "H:/data/"

    print("reading CIMSDATA_20230801_ext2 feather data")
    df_cims = pd.read_feather(basepath+"python_pandas/CIMS/"+"CIMSDATA_20230801_ext2.ftr")
    # print(df_cims.shape)

    df_pop = read_population_NL_all()

    versionstr = "_v2"
    prik_nummer = 1

    year = 2023

    # filename_core = "GBAPERSOON2022_presentinyear_incldead"
    # print("reading " + filename_core + " feather data")
    # df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")
    #DEBUG Would be better to use geboortejaar!? Minder gedoe met veranderende leeftijd in een jaar, en vergelijking
    # met GBA gegevens in een vorig jaar en zo
    # nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=(age_from-1)) & (df_p['leeftijd_in_ditjaar']<(age_to-1)) ] )

    age_list = []
    perc_list = []
    for age in range(0,120,10):
        age_from =age
        age_to = age+10
        age_list.append(int((age_from+age_to)/2))

        nr_p_ag = get_nr_people_fromto_age(df_pop, year, age_from, age_to)
        # nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] )
        print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))

        # who has received a vaccination and is in that age group?
        df_fc = df_cims[    (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                            (df_cims["prik_nummer"] == prik_nummer) ]
        nr_vaxed_agegroup = df_fc["RINPERSOON"].nunique()
        nr_unvaxed_agegroup = nr_p_ag - nr_vaxed_agegroup
        print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup))
        print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup))
        nr_pop_agegroup = nr_unvaxed_agegroup + nr_vaxed_agegroup
        print("sum: " + str(nr_pop_agegroup))

        if nr_pop_agegroup>1000:
            perc_vax = float(nr_vaxed_agegroup)/float(nr_pop_agegroup) * 100.0
        else:
            perc_vax = np.nan
        perc_list.append(perc_vax)
        

    plt.bar(age_list,perc_list, color = 'b', width=5)

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    # plt.hist([dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)
    plt.xlabel('age category')
    plt.ylabel('vaccination rate')
    # plt.ylabel('perc. dead in age group')
    # plt.xticks(range(1,52,5))
    plt.xticks(age_list)
    plt.grid()
    # plt.legend()
    plt.title("Percentage C19-vaccinated (injection >= " + str(prik_nummer) +") per age group")
    
    plt.savefig("H:/data/output/plots/vaccinationrate_inj" + str(prik_nummer) + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    # plt.savefig("H:/data/plots/deaths_vaccines_" + yearsstr + "_" + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    # plt.savefig("H:/data/plots/hist_deaths_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 