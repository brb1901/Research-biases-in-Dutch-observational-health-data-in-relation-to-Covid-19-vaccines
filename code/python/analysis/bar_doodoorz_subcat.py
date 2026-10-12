import pandas as pd
import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


def run_main():
    basepath = "H:/data/"

    age_from = 10 # 0 #50 #  65 # 50 # 15 # 65 # 10 # 15 # 60 50 40 # 0 #
    age_to = 30 # 50 #65 # 125 # 65 # 50 # 125 # 50 # 45 # 90 75 65 # 50 #
    versionstr = "_v4"
    yearsstr = "2015-2022" # "2021" #
    wid = 0.07
    multiplier = 0
    # ICD_cats_list = ['C', 'I', 'U', 'F', 'J', 'R', 'G', 'W', 'K', 'N', 'E', 'D', 'A', 'X', 'M', 'B', 'Y', 'L', 'V', 'Q', 'H', 'O']
    # ICD_cats_list = ['I0', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
    # firstletter_select = 'I'
    # ICD_cats_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    # firstletter_select = 'C'
    # ICD_cats_list = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']
    # firstletter_select = 'R'
    # ICD_cats_list = ['X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9']
    # firstletter_select = 'X'
    ICD_cats_list = ['G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9']
    firstletter_select = 'G'
    nr_categories = len(ICD_cats_list)
    x = np.arange(nr_categories)
    years_list = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    nr_items = len(years_list)
    for year in years_list:
        # year = 2021
        yearstr = str(year)
        print(yearstr)
        offset = wid * multiplier
        multiplier += 1
        causes_number_array = np.array([0]*nr_categories, dtype=int)

        filename_core = "DOODOORZ" + yearstr 
        print("reading " + filename_core + " feather data")
        df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

        # print("making new column of first letters of ICD10 cause of death")
        # df_do['firstletter_ICD'] = df_do['UCCODE'].str[0]
        df_do['firstletters_ICD'] = df_do['UCCODE'].str[:2]

        filename_core = "GBAPERSOON" + yearstr + "_presentinyear_incldead"
        print("reading " + filename_core + " feather data")
        df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")

        df_pf = df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] 
        # print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))

        # select those deaths from doodoorzaken that we can also find in the filtered GBA Persoon data for the correct age group
        # AND select only 1 main category of deaths
        df_do_rightage = df_do[ df_do['RINPERSOON'].isin(df_pf['RINPERSOON']) & df_do['firstletters_ICD'].str.startswith(firstletter_select)  ] # & df_do['firstletter_ICD']==firstletter_select

        # df_do_rightage.firstletter_ICD.value_counts().plot(kind='bar')

        data_thisyear = df_do_rightage.firstletters_ICD.value_counts()
        # print(data_thisyear)
        # print(data_thisyear.shape)

        x_cat = data_thisyear.index.tolist()
        y= data_thisyear.values
        ind = [ICD_cats_list.index(i) for i in x_cat]
        # print(ind)

        causes_number_array[ind] = y
        # print(causes_number_array)
        # print(x_cat)
        # # # print(x)
        # print(y)

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
        
    plt.title("Causes of death " + yearsstr + ", age group " + str(age_from) +"-" + str(age_to))
    plt.legend()
    plt.xticks(x + (wid*(float(nr_items)/2.0)), ICD_cats_list)

    plt.savefig("H:/data/plots/subcat_" + firstletter_select + "_causes_of_death_" + yearsstr + ", age group " + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show() # block=False

if __name__ == '__main__':
    run_main()
    


 