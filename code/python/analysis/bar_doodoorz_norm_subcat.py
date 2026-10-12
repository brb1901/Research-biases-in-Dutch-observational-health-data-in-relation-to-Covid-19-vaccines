import pandas as pd
import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from generic_functions import read_population_NL_all, read_population_NL_men, read_population_NL_women, get_nr_people_fromto_age


def run_main():
    basepath = "H:/data/"

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    df_pop = read_population_NL_all()

    age_from = 0 # 70 # 0 # 15 # 65 # 10 # 15 # 60 50 40 # 0 # 65 # 50 # 
    age_to = 40 # 110 # 50 # 125 # 50 # 45 # 90 75 65 # 50 # 125 # 65 # 
    versionstr = "_v5"
    yearsstr = "2018-2022" # "2021" #
    wid = 0.07 # 0.15
    multiplier = 0
    # ICD_cats_list = ['C', 'I', 'U', 'F', 'J', 'R', 'G', 'W', 'K', 'N', 'E', 'D', 'A', 'X', 'M', 'B', 'Y', 'L', 'V', 'Q', 'H', 'O']
    ICD_cats_list = ['I0', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
    firstletter_select = 'I'
    # ICD_cats_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    # firstletter_select = 'C'
    # ICD_cats_list = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']
    # firstletter_select = 'R'
    nr_categories = len(ICD_cats_list)
    x = np.arange(nr_categories)
    years_list = range(2013,2023)  #[2018, 2019, 2020, 2021, 2022]
    nr_items = len(years_list)
    for year in years_list:
        # year = 2021
        yearstr = str(year)
        offset = wid * multiplier
        multiplier += 1
        causes_number_array = np.array([0]*nr_categories, dtype=float)

        filename_core = "DOODOORZ" + yearstr 
        print("reading " + filename_core + " feather data")
        df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

        print("making new column of first letters of ICD10 cause of death")
        # df_do['firstletter_ICD'] = df_do['UCCODE'].str[0]
        df_do['firstletters_ICD'] = df_do['UCCODE'].str[:2]

        nr_p_ag = get_nr_people_fromto_age(df_pop, year, age_from, age_to)
        print("Number of people in this age group in this year: " + str(nr_p_ag))

        # filename_core = "GBAPERSOON" + yearstr + "_presentinyear_incldead"
        # print("reading " + filename_core + " feather data")
        # df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")

        # df_pf = df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] 
        # nr_p_ag = len(df_pf)
        # # print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))

        df_fo = df_o[ (df_o["jaar_overlijden"] == year) & 
                            (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ] 

        # select those deaths from doodoorzaken that we can also find in the filtered GBA Persoon data for the correct age group
        # AND select only 1 main category of deaths
        df_do_rightage = df_do[ df_do['RINPERSOON'].isin(df_fo['RINPERSOON']) & df_do['firstletters_ICD'].str.startswith(firstletter_select)  ] # & df_do['firstletter_ICD']==firstletter_select

        # df_do_rightage.firstletter_ICD.value_counts().plot(kind='bar')

        data_thisyear = df_do_rightage.firstletters_ICD.value_counts()
        print(data_thisyear)
        print(data_thisyear.shape)

        x_cat = data_thisyear.index.tolist()
        y= data_thisyear.values
        ind = [ICD_cats_list.index(i) for i in x_cat]
        print(ind)
        normfactor = 100000.0/float(nr_p_ag)
        norm_y = [float(y_val) * normfactor for y_val in y]

        causes_number_array[ind] = norm_y
        # print(causes_number_array)
        print(x_cat)
        # # print(x)
        print(y)

        
        # plt.bar(x + offset, y, width=wid, label=yearstr) # , color = 'b'
        plt.bar(x + offset, causes_number_array, width=wid, label=yearstr) # , color = 'b'

        # df_do_rightage = df_do_rightage.groupby('firstletter_ICD').sum().sort_values
        # cause_freq = df_do_rightage['firstletter_ICD'].value_counts()
            
        # plt.bar(age_list,perc_list, color = 'b', width=5)

        # plt.title("Causes of death " + yearstr + ", age group " + str(age_from) +"-" + str(age_to))
        # # plt.legend()
        # # plt.xticks(x, x_cat)

        # # plt.savefig("H:/data/plots/causes_of_death_" + yearstr + ", age group " + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")

        # plt.show() # block=False
        
    plt.title("Causes of death (per 100.000) " + yearsstr + ", age group " + str(age_from) +"-" + str(age_to))
    plt.legend()
    plt.xticks(x + (wid*(float(nr_items)/2.0)), ICD_cats_list)

    plt.savefig("H:/data/output/plots/subcat_" + firstletter_select + "_causes_of_death_norm_" + yearsstr + ", age group " + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show() # block=False

if __name__ == '__main__':
    run_main()
    


 