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

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    # df_pop = read_population_NL_all()

    versionstr = "_v2"
    # prik_nummer = 1

    refyear = 2021

    df_fo = df_o[ (df_o["jaar_overlijden"] < refyear)  ] # year &  (df_o['RINPERSOON'].isin(df_p['RINPERSOON']))
    nr_deaths_before_refyear = len(df_fo)
    print("Number of deaths before refyear: " + str(nr_deaths_before_refyear))

    # filename_core = "GBAPERSOON2022_presentinyear_incldead"
    # print("reading " + filename_core + " feather data")
    # df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")
    #DEBUG Would be better to use geboortejaar!? Minder gedoe met veranderende leeftijd in een jaar, en vergelijking
    # met GBA gegevens in een vorig jaar en zo
    # nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=(age_from-1)) & (df_p['leeftijd_in_ditjaar']<(age_to-1)) ] )

    print("reading GBAPERSOON_trackable_years2018-2022_ext feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_years2018-2022_ext.ftr")
    print(df_p.shape)

    df_p = df_p[~df_p['RINPERSOON'].isin(df_fo['RINPERSOON'])]
    print("After removing deaths before refyear: ")
    print(df_p.shape)        
    print()

    age_list = []
    birthyear_list = []
    perc_list = []
    cats_list = []
    stepsize = 10
    for birthyear in range(2010,1909,-stepsize):
    # stepsize = 100
    # for birthyear in range(1910,2009,stepsize):
        birthyear_from = birthyear
        birthyear_to = birthyear_from + stepsize
        birthyear_list.append(int((birthyear_from+birthyear_to)/2))

        # catsubstr = str(birthyear_from) + "-" + str(birthyear_to)
        catsubstr = str(int((birthyear_from+birthyear_to)/2))
        cats_list.append(catsubstr)

        age_from = refyear - birthyear_to
        age_to = refyear - birthyear_from
        age_list.append(int((age_from+age_to)/2))

        # nr_p_ag = get_nr_people_fromto_age(df_pop, year, age_from, age_to)
        # nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] )
        # print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))

        nr_p_ag = len( df_p[ (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) ] )
        print(str(birthyear_from) + "-" + str(birthyear_to) + ": " + str(nr_p_ag))
        print("age (in 2021): " + str(age_from) + "-" + str(age_to) )

        # who has received a vaccination and is in that age group?
        df_fc = df_cims[  (df_cims['jaar_geb']>=birthyear_from) & (df_cims['jaar_geb']<birthyear_to) ] # & (df_cims["prik_nummer"] == prik_nummer)
        df_fc = df_fc[df_fc['RINPERSOON'].isin(df_p['RINPERSOON'])] # gevaccineerden gevonden in trackable GBA dataset
        nr_vaxed_agegroup = df_fc["RINPERSOON"].nunique()
        nr_unvaxed_agegroup = nr_p_ag - nr_vaxed_agegroup
        print("nr_vaxed_agegroup: " + str(nr_vaxed_agegroup))
        print("nr_unvaxed_agegroup: " + str(nr_unvaxed_agegroup))
        nr_pop_agegroup = nr_unvaxed_agegroup + nr_vaxed_agegroup
        print("sum (sanity check): " + str(nr_pop_agegroup))

        if nr_pop_agegroup>1000:
            perc_vax = float(nr_vaxed_agegroup)/float(nr_pop_agegroup) * 100.0
        else:
            perc_vax = np.nan
        perc_list.append(perc_vax)
        print("perc_vax: " + str(perc_vax))
        print()

    # x = np.arange(len(perc_list))
    plt.bar(age_list, perc_list, color = 'b', width=5) # 
    plt.xticks(age_list, cats_list)
    # plt.grid(None)

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    # plt.hist([dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)
    plt.xlabel('birth-year category')
    plt.ylabel('vaccination rate')
    # plt.ylabel('perc. dead in age group')
    # plt.xticks(range(1,52,5))
    # plt.xticks(birthyear_list)
    # plt.grid()
    # plt.legend()
    plt.title("Percentage C19-vaccinated per birth-year group")
    # plt.title("Percentage C19-vaccinated (injection >= " + str(prik_nummer) +") per age group")
    
    # plt.savefig("H:/data/output/plots/vaccinationrate_BY_trackable" + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 