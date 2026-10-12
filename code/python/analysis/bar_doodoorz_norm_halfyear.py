import pandas as pd
import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np


def run_main():
    basepath = "H:/data/"

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    # print("reading CIMSDATA_20230801_ext2 feather data")
    # df_cims = pd.read_feather(basepath+"python_pandas/CIMS/"+"CIMSDATA_20230801_ext2.ftr")

    age_from = 65 # 50 #15 # 65 # 10 # 15 # 60 50 40 # 65 # 50 # 
    age_to = 125 #65 # 50 # 125 # 50 # 45 # 90 75 65 # 125 # 65 # 
    versionstr = "_hy_v3"
    yearsstr = "2018-2022" # "2021" #
    # vaxedstatus = True # False # 
    # vaxlabel = "vaccinated" # "unvaccinated" # 
    wid = 0.07 # 0.15
    multiplier = 0
    ICD_cats_list = ['C', 'I', 'U', 'F', 'J', 'R', 'G', 'W', 'K', 'N', 'E', 'D', 'A', 'X', 'M', 'B', 'Y', 'L', 'V', 'Q', 'H', 'O']
    nr_categories = len(ICD_cats_list)
    x = np.arange(nr_categories)
    years_list = [2018, 2019, 2020, 2021, 2022]
    nr_items = len(years_list)*2
    for year in years_list:
        # year = 2021
        yearstr = str(year)
        print(yearstr)
        filename_core = "DOODOORZ" + yearstr 
        print("reading " + filename_core + " feather data")
        df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

        print("making new column of first letters of ICD10 cause of death")
        df_do['firstletter_ICD'] = df_do['UCCODE'].str[0]

        filename_core = "GBAPERSOON" + yearstr + "_presentinyear_incldead"
        print("reading " + filename_core + " feather data")
        df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")

        df_pf = df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] 
        # print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))
        nr_p_ag = len(df_pf)

        for yearhalf in [1, 2]:
            print(yearhalf)
            if yearhalf == 1:
                maand_overlijden_min = 1
                maand_overlijden_max = 6
                # date_to = date(year,6,30)
            else:
                maand_overlijden_min = 7
                maand_overlijden_max = 12
                # date_to = date(year,6,30)
        
            offset = wid * multiplier
            multiplier += 1
            causes_number_array = np.array([0]*nr_categories, dtype=float)

            df_fo = df_o[ (df_o["jaar_overlijden"] == year) & 
                            (df_o["maand_overlijden"] >= maand_overlijden_min) & (df_o["maand_overlijden"] <= maand_overlijden_max) &
                            (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]
            nr_deaths_all_halfyear = len(df_fo)
            print("Number of deaths in this age group in this half-year: " + str(nr_deaths_all_halfyear))     

            df_fo_notfounddo = df_fo[~df_fo['RINPERSOON'].isin(df_do['RINPERSOON'])]
            nr_notfoundindoodoorz = len(df_fo_notfounddo)
            nr_deaths_all_halfyear -= nr_notfoundindoodoorz
            nr_p_ag -= nr_notfoundindoodoorz
            print("Number of deaths in this age group in this half-year (after correction): " + str(nr_deaths_all_halfyear))  

            # select those Doodoorzaken that we can also find in the filtered GBA Persoon data AND died in the correct half-year for the correct age group                
            df_do_rightage = df_do[ df_do['RINPERSOON'].isin(df_pf['RINPERSOON']) & df_do['RINPERSOON'].isin(df_fo['RINPERSOON']) ]

            # df_do_rightage.firstletter_ICD.value_counts().plot(kind='bar')

            data_thishalfyear = df_do_rightage.firstletter_ICD.value_counts()
            # # print(data_thishalfyear)
            # # print(data_thishalfyear.shape)

            x_cat = data_thishalfyear.index.tolist()
            y= data_thishalfyear.values
            ind = [ICD_cats_list.index(i) for i in x_cat]
            # print(ind)
            normfactor = 100000.0/float(nr_p_ag)
            
            norm_y = [float(y_val) * normfactor for y_val in y]

            causes_number_array[ind] = norm_y
            # print(causes_number_array)
            # print(x_cat)
            # # print(x)
            # # print(y)

            
            # plt.bar(x + offset, y, width=wid, label=yearstr) # , color = 'b'
            plt.bar(x + offset, causes_number_array, width=wid, label=yearstr+"-"+str(yearhalf)) # , color = 'b'

            # df_do_rightage = df_do_rightage.groupby('firstletter_ICD').sum().sort_values
            # cause_freq = df_do_rightage['firstletter_ICD'].value_counts()
                
            # plt.bar(age_list,perc_list, color = 'b', width=5)

            # plt.title("Causes of death " + yearstr + ", age group " + str(age_from) +"-" + str(age_to))
            # # plt.legend()
            # # plt.xticks(x, x_cat)

            # # plt.savefig("H:/data/plots/causes_of_death_" + yearstr + ", age group " + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")

            # plt.show() # block=False
        
    plt.title("Causes of death " + yearsstr + ", per 100,000, age group " + str(age_from) +"-" + str(age_to))
    plt.legend()
    plt.xticks(x + (wid*(float(nr_items)/2.0)), ICD_cats_list)
    plt.xlabel('ICD10 codes')
    plt.ylabel('number of deaths (per 100,000)')

    plt.savefig("H:/data/plots/causes_of_death_norm_" + yearsstr + ", age group " + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show() # block=False

if __name__ == '__main__':
    run_main()
    


 