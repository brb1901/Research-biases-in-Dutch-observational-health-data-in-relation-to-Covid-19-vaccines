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

    # age_from = 65 # 50 #15 # 65 # 10 # 15 # 60 50 40 # 65 # 50 # 
    # age_to = 125 #65 # 50 # 125 # 50 # 45 # 90 75 65 # 125 # 65 # 
    versionstr = "_hy_v1"
    yearsstr = "2018-2022" # "2021" #
    sex = 2 # 1  # GBAGESLACHT: 1 = M, 2 = F
    sexstr = "F" # "M"
    # vaxedstatus = True # False # 
    # vaxlabel = "vaccinated" # "unvaccinated" # 
    wid = 0.07 # 0.15
    multiplier = 0
    # age_cats_list = range(5,115,10)
    # age_cats_list = range(85,115,10)
    # age_cats_list = range(55,85,10)
    age_cats_list = range(5,55,10)
    nr_categories = len(age_cats_list)
    x = np.arange(nr_categories)
    years_list = [2018, 2019, 2020, 2021, 2022]
    nr_items = len(years_list)*2
    for year in years_list:
        # year = 2021
        yearstr = str(year)
        print(yearstr)

        filename_core = "GBAPERSOON" + yearstr + "_presentinyear_incldead"
        print("reading " + filename_core + " feather data")
        df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")

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
            deaths_number_array = np.array([0]*nr_categories, dtype=float)

            ind = 0
            for age in age_cats_list:
                age_from = age - 5
                age_to = age + 5
                # print(age_from)
                # print(age_to)

                df_pf = df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) & (df_p['GBAGESLACHT'].astype(int)==sex) ] 
                # print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))
                nr_p_ag = len(df_pf)
                normfactor = 100000.0/float(nr_p_ag)

                df_fo = df_o[ (df_o["jaar_overlijden"] == year) & 
                                (df_o["maand_overlijden"] >= maand_overlijden_min) & (df_o["maand_overlijden"] <= maand_overlijden_max) &
                                (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]                

                # select those Doodoorzaken that we can also find in the filtered GBA Persoon data AND died in the correct half-year for the correct age group                
                df_fo_rightsex = df_fo[ df_fo['RINPERSOON'].isin(df_pf['RINPERSOON']) ]
                nr_deaths_all_halfyear = len(df_fo_rightsex)
                # print("Number of deaths in this age group AND for this gender in this half-year: " + str(nr_deaths_all_halfyear))

                norm_y = float(nr_deaths_all_halfyear) * normfactor
                deaths_number_array[ind] = norm_y
                ind += 1
            
            # print(deaths_number_array)
            # print(x_cat)
            # # print(x)
            # # print(y)
            
            # plt.bar(x + offset, y, width=wid, label=yearstr) # , color = 'b'
            plt.bar(x + offset, deaths_number_array, width=wid, label=yearstr+"-"+str(yearhalf)) # , color = 'b'
        
    plt.title("Number of deaths " + yearsstr + " per 100,000 for age groups, " + sexstr )
    plt.legend()
    plt.xticks(x + (wid*(float(nr_items)/2.0)), age_cats_list)
    plt.xlabel('age groups')
    plt.ylabel('number of deaths (per 100,000)')

    plt.savefig("H:/data/plots/bar_deaths_norm_" + yearsstr + "_young_agegroups_" + sexstr + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show() # block=False

if __name__ == '__main__':
    run_main()
    


 