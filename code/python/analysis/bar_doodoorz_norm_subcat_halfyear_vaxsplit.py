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

    print("reading CIMSDATA_20230801_ext2 feather data")
    df_cims = pd.read_feather(basepath+"python_pandas/CIMS/"+"CIMSDATA_20230801_ext2.ftr")

    df_pop = read_population_NL_all()

    age_from = 10  # 65 # 10 # 15 # 60 50 40 # 65 # 50 #  15 # 
    age_to = 30 # 125 # 50 # 45 # 90 75 65 # 125 # 65 # 50 # 
    # ylim_max = 121.0
    versionstr = "_hy_v9"
    yearsstr = "2017-2022" # "2021" #
    vaxedstatus = True # False # 
    vaxlabel = "vaccinated" # "unvaccinated" #  
    wid = 0.07 # 0.15
    multiplier = 0
    # ICD_cats_list = ['C', 'I', 'U', 'F', 'J', 'R', 'G', 'W', 'K', 'N', 'E', 'D', 'A', 'X', 'M', 'B', 'Y', 'L', 'V', 'Q', 'H', 'O']
    ICD_cats_list = ['I0', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
    firstletter_select = 'I'
    # ICD_cats_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    # firstletter_select = 'C'
    # ICD_cats_list = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']
    # firstletter_select = 'R' # 'I' # 
    # ICD_cats_list = ['X0', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9']
    # firstletter_select = 'X'

    nr_categories = len(ICD_cats_list)
    x = np.arange(nr_categories)
    years_list = [2017, 2018, 2019, 2020, 2021, 2022] # 2015, 2016, 
    nr_items = len(years_list)*2
    for year in years_list:
        # year = 2021
        yearstr = str(year)
        print(yearstr)
        filename_core = "DOODOORZ" + yearstr 
        print("reading " + filename_core + " feather data")
        df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

        print("making new column of first letters of ICD10 cause of death")
        # df_do['firstletter_ICD'] = df_do['UCCODE'].str[0]
        df_do['firstletters_ICD'] = df_do['UCCODE'].str[:2]

        # filename_core = "GBAPERSOON" + yearstr + "_presentinyear_incldead"
        # print("reading " + filename_core + " feather data")
        # df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")

        # df_pf = df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] 
        # # print(str(age) + "-" + str(age_to+1) + ": " + str(nr_p_ag))
        # nr_p_ag = len(df_pf)
        nr_p_ag = get_nr_people_fromto_age(df_pop, year, age_from, age_to)

        for yearhalf in [1, 2]:
            print(yearhalf)
            if yearhalf == 1:
                maand_overlijden_min = 1
                maand_overlijden_max = 6
                date_to = date(year,6,30)
            else:
                maand_overlijden_min = 7
                maand_overlijden_max = 12
                date_to = date(year,12,31)
        
            offset = wid * multiplier
            multiplier += 1
            causes_number_array = np.array([0]*nr_categories, dtype=float)

            df_fo = df_o[ (df_o["jaar_overlijden"] == year) & 
                            (df_o["maand_overlijden"] >= maand_overlijden_min) & (df_o["maand_overlijden"] <= maand_overlijden_max) &
                            (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]
            nr_deaths_all_halfyear = len(df_fo)
            print("Number of deaths in this age group in this half-year: " + str(nr_deaths_all_halfyear))        

            if (year==2021 ) or (year>2021): #and yearhalf==2
                # who has received a vaccination before the end of this period, and is in that age group?
                df_fc = df_cims[ (df_cims["datetimeobj_prik"] <= (date_to)) &  #  - timedelta(weeks = 2)
                                (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to)  ]
                
                nr_vaxed_agegroup_untilthen = df_fc["RINPERSOON"].nunique()
                nr_unvaxed_agegroup_untilthen = nr_p_ag - nr_vaxed_agegroup_untilthen

                # select those deaths that we can also find in CIMS
                df_ovax = df_fo[df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]
                nr_deaths_vax = df_ovax['RINPERSOON'].nunique()
                # select those vaccinated deaths that we can find in DOODOORZ
                df_do_vax = df_do[df_do['RINPERSOON'].isin(df_ovax['RINPERSOON'])]
                nr_vax_notfoundindoodoorz = nr_deaths_vax - len(df_do_vax)
                print("Vaccinated: NOT found in DOODOORZ: " + str(nr_vax_notfoundindoodoorz))
                nr_vaxed_agegroup_untilthen -= nr_vax_notfoundindoodoorz
                nr_deaths_vax -= nr_vax_notfoundindoodoorz

                nr_deaths_novax = nr_deaths_all_halfyear - nr_deaths_vax
                df_onovax = df_fo[~df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]
                df_do_novax = df_do[df_do['RINPERSOON'].isin(df_onovax['RINPERSOON'])]
                nr_novax_notfoundindoodoorz = nr_deaths_novax - len(df_do_novax)
                print("Not (registered as) vaccinated: NOT found in DOODOORZ: " + str(nr_novax_notfoundindoodoorz))
                nr_unvaxed_agegroup_untilthen -= nr_novax_notfoundindoodoorz
                nr_deaths_novax -= nr_novax_notfoundindoodoorz

            # select those Doodoorzaken that we can also find in the filtered GBA Persoon data AND died in the correct half-year (AND possibly CIMS) for the correct age group                
            # df_do_rightage = df_do[ df_do['RINPERSOON'].isin(df_pf['RINPERSOON']) & df_do['firstletters_ICD'].str.startswith(firstletter_select)  ]
            if (year==2021 and yearhalf==2) or (year>2021):
                if vaxedstatus is True:
                    df_do_rightage = df_do[ df_do['firstletters_ICD'].str.startswith(firstletter_select) & df_do['RINPERSOON'].isin(df_fo['RINPERSOON']) & df_do['RINPERSOON'].isin(df_fc['RINPERSOON']) ]
                else:
                    df_do_rightage = df_do[ df_do['firstletters_ICD'].str.startswith(firstletter_select) & df_do['RINPERSOON'].isin(df_fo['RINPERSOON']) & ~df_do['RINPERSOON'].isin(df_fc['RINPERSOON']) ]
            else:
                df_do_rightage = df_do[ df_do['firstletters_ICD'].str.startswith(firstletter_select) & df_do['RINPERSOON'].isin(df_fo['RINPERSOON']) ]

            # df_do_rightage.firstletter_ICD.value_counts().plot(kind='bar')

            # data_thishalfyear = df_do_rightage.firstletter_ICD.value_counts()
            data_thishalfyear = df_do_rightage.firstletters_ICD.value_counts()
            # # print(data_thishalfyear)
            # # print(data_thishalfyear.shape)

            x_cat = data_thishalfyear.index.tolist()
            y= data_thishalfyear.values
            ind = [ICD_cats_list.index(i) for i in x_cat]
            # print(ind)

            if (year==2021 ) or (year>2021): # and yearhalf==2
                if vaxedstatus is True:
                    normfactor = 100000.0/float(nr_vaxed_agegroup_untilthen)
                else:
                    normfactor = 100000.0/float(nr_unvaxed_agegroup_untilthen)
            else:
                if(nr_p_ag>0):
                    normfactor = 100000.0/float(nr_p_ag)            
                else:
                    normfactor = np.nan
            
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
        
    # plt.ylim(0.0, ylim_max)
    plt.title("Causes of death " + yearsstr + ", per 100,000, age group " + str(age_from) +"-" + str(age_to) + ", " + vaxlabel)
    plt.legend()
    plt.xticks(x + (wid*(float(nr_items)/2.0)), ICD_cats_list)
    plt.xlabel('ICD10 codes')
    plt.ylabel('number of deaths (per 100,000)')

    plt.savefig("H:/data/output/plots/subcat_" + firstletter_select + "_causes_of_death_norm_hy_" + yearsstr + ", age group " + str(age_from) +"-" + str(age_to) + "_" + vaxlabel + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show() # block=False

if __name__ == '__main__':
    run_main()
    


 