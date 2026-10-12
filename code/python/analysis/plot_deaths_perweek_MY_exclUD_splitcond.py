import pandas as pd
import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from generic_functions import read_population_NL_all, read_population_NL_men, read_population_NL_women, get_nr_people_fromto_age


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    # basepath_dta = basepath+"stata/GBA/"
    # basepath_ftr = basepath+"python_pandas/GBA/"
    # basepath_csv = basepath+"csv/GBA/"

    print("reading GBAOVERLIJDEN2022_ext2 feather data")
    df_o = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAOVERLIJDEN2022_ext2.ftr")

    print("reading CIMSDATA_20230801_ext2 feather data")
    df_cims = pd.read_feather(basepath+"python_pandas/CIMS/"+"CIMSDATA_20230801_ext2.ftr")
    # print(df_cims.shape)

    # DOODOORZ2017-2022.ftr
    filename_core = "DOODOORZ2017-2022" 
    print("reading " + filename_core + " feather data")
    df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

    df_pop = read_population_NL_all()

    # for year in [2018, 2019, 2020, 2021, 2022]:
    year = 2020 # 2018 # 2019 # 2018 2021 # 
    year_tostop = 2023 # 2022 # 
    nr_years = year_tostop - year
    # 
    yearsstr = "2020-2022" # "2021" #
    year_prev = year - 1
    
    # print(yearstr)

    age_from = 50 #70 # 10 # 40 # 70 #  10 # 65 # 10 # 15 # 60 50 40 # 
    age_to = 70 #90 # 30 # 70 # 90 # 50 # 125 # 50 # 45 # 90 75 65 # 

    vaxnormfactor = 20000 # 4000000 #20000 #200000 #5000 # 8000 100000 4000

    versionstr = "_v8"

    date_from = date(year,1,1)
    date_to = date_from + timedelta(weeks = 1)

    weeknr = 1
    nr_deaths_list = []
    nr_deaths_vax_list = []
    nr_deaths_novax_list = []
    perc_deaths_vax_list = []
    perc_deaths_novax_list = []
    perc_deaths_all_list = []
    # perc_deaths_unknown_list = []
    nr_vax1_list = []
    # nr_vax2_list = []
    # nr_vax3_list = []
    # nr_vax4_list = []
    # nr_vax5_list = []
    weeknr_list = []

    perc_U_vax_list = []
    perc_I_vax_list = []
    perc_C_vax_list = []
    perc_G_vax_list = []
    perc_R_vax_list = []
    perc_U_unvax_list = []
    perc_I_unvax_list = []
    perc_C_unvax_list = []
    perc_G_unvax_list = []
    perc_R_unvax_list = []

    while year<year_tostop: # and weeknr <=6:
        if year > year_prev:
            yearstr = str(year)
            print(year)

            nr_p_ag = get_nr_people_fromto_age(df_pop, year, age_from, age_to)
            print("Number of people alive and present in this age group beginning of the year: " + str(nr_p_ag))

            df_fo = df_o[ (df_o["jaar_overlijden"] == year) & 
                        (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]
            nr_deaths_all_year = len(df_fo)
            print("Number of deaths in this age group in this year: " + str(nr_deaths_all_year))
            # nr_p_ag += nr_deaths_all_year
            # print("Number of people in this age group in this year: " + str(nr_p_ag))

            # who has received a vaccination before the start of this period, and is in that age group?
            df_fc = df_cims[ (df_cims["datetimeobj_prik"] < (date_from)) &  #  - timedelta(weeks = 2)
                                (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                                (df_cims["prik_nummer"] == 1) ]
            nr_vaxed_agegroup_untilthen = df_fc["RINPERSOON"].nunique()
            nr_unvaxed_agegroup_untilthen = nr_p_ag - nr_vaxed_agegroup_untilthen
            print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup_untilthen))
            print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup_untilthen))
            print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))


        print(weeknr)
        print(date_from)
        # print("selecting deaths in " + yearstr)
        df_fo = df_o[ (df_o["datetimeobj_overlijden"] >= date_from) & (df_o["datetimeobj_overlijden"] < date_to) &
                      (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]
        # nr_deaths_all = len(df_fo)
        nr_deaths_all = df_fo["RINPERSOON"].nunique()
        nr_deaths_list.append(nr_deaths_all)

        # nr_vaxed_agegroup_untilthen = len(df_fc)        
        
        # who has received a FIRST vaccination IN this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == 1) ]
        # nr_vaxed_agegroup_thisweek = len(df_fc) 
        nr_vaxed_agegroup_thisweek = df_fc["RINPERSOON"].nunique()
        nr_vaxed_agegroup_untilthen += nr_vaxed_agegroup_thisweek
        if nr_vaxed_agegroup_untilthen==0:
            nr_vaxed_agegroup_untilthen=1

        # who has received ANY vaccination IN this week, and is in that age group?
        # No, who has received the FIRST vaccination in this week?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == 1)  ]
        nr_anyvaxed_agegroup_thisweek = df_fc["RINPERSOON"].nunique()
        nr_vax1_list.append(float(nr_anyvaxed_agegroup_thisweek)/vaxnormfactor)

        # who has received a vaccination before the end of this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < (date_to)) &  #  - timedelta(weeks = 2)
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] <= 2) ]

        # select those deaths that we can also find in CIMS, vaccinations only before the end of this week
        df_ovax = df_fo[df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]
        # df['Rinpersoon'].nunique()
        # nr_deaths_vax = len(df_ovax)
        nr_deaths_vax = df_ovax['RINPERSOON'].nunique()
    
        nr_unvaxed_agegroup_untilthen = nr_unvaxed_agegroup_untilthen - nr_vaxed_agegroup_thisweek
        # nr_vax1_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0  100000.0
        nr_deaths_novax = nr_deaths_all - nr_deaths_vax
        print("nr_vaxed_agegroup_untilthen (BEFORE CLEANUP): " + str(nr_vaxed_agegroup_untilthen))
        print("nr_unvaxed_agegroup_untilthen (BEFORE CLEANUP): " + str(nr_unvaxed_agegroup_untilthen))
        print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))
        
        print("nr_deaths_vax (BEFORE CLEANUP): " + str(nr_deaths_vax))
        print("nr_deaths_novax (BEFORE CLEANUP): " + str(nr_deaths_novax))
        print("nr_deaths_all: " + str(nr_deaths_all))

        perc_deaths_all = float(nr_deaths_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100000.0
        ##DEBUG!!: now only HEART deaths in all!!
        # perc_deaths_all = float(nr_heartdeaths_vax + nr_heartdeaths_novax)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100000.0
        perc_deaths_all_list.append(perc_deaths_all)

        # select those vaccinated deaths that we can find in DOODOORZ
        df_do_vax = df_do[df_do['RINPERSOON'].isin(df_ovax['RINPERSOON'])]
        nr_5 = nr_deaths_vax - len(df_do_vax)
        print("Vaccinated: found in DOODOORZ: " + str(len(df_do_vax)))
        print("Vaccinated: NOT found in DOODOORZ: " + str(nr_5))
        nr_5_vax = nr_5
        print("Vaccinated: nr_5 per 100000: " + str(float(nr_5)/float(nr_vaxed_agegroup_untilthen) * 100000.0))

        nr_vaxed_agegroup_untilthen -= nr_5_vax
        nr_deaths_vax -= nr_5_vax

        nr_U_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('U')] ) # Covid and similar
        nr_I_ICD10 = len( df_do_vax[ (df_do_vax['UCCODE'].str.startswith('I')) ] ) # heart diseases
        nr_C_ICD10 = len( df_do_vax[ (df_do_vax['UCCODE'].str.startswith('C')) ] ) # cancer, immunodeficiencies
        nr_G_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('J')] ) 
        nr_R_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('R')] ) # unexplained, sudden deaths

        perc_U_vax_list.append(float(nr_U_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_I_vax_list.append(float(nr_I_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_C_vax_list.append(float(nr_C_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_G_vax_list.append(float(nr_G_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_R_vax_list.append(float(nr_R_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)

        # select deaths that we do not find in CIMS -> assume those are UNvaccinated
        df_onovax = df_fo[~df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]
        # select those UNvaccinated deaths that we can find in DOODOORZ
        df_do_novax = df_do[df_do['RINPERSOON'].isin(df_onovax['RINPERSOON'])]

        nr_5 = nr_deaths_novax - len(df_do_novax)
        nr_5_novax = nr_5        
        print("Unvaccinated: found in DOODOORZ: " + str(len(df_do_novax)))
        print("Unvaccinated: NOT found in DOODOORZ: " + str(nr_5))
        print("Unvaccinated: nr_5 per 100000: " + str(float(nr_5)/float(nr_unvaxed_agegroup_untilthen) * 100000.0))
        nr_unvaxed_agegroup_untilthen -= nr_5_novax
        nr_deaths_novax -= nr_5_novax

        nr_U_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('U')] )
        nr_I_ICD10 = len( df_do_novax[ (df_do_novax['UCCODE'].str.startswith('I'))] )
        nr_C_ICD10 = len( df_do_novax[ (df_do_novax['UCCODE'].str.startswith('C'))] ) # cancer, immunodeficiencies
        nr_G_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('J')] )
        nr_R_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('R')] )

        perc_U_unvax_list.append(float(nr_U_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_I_unvax_list.append(float(nr_I_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_C_unvax_list.append(float(nr_C_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_G_unvax_list.append(float(nr_G_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_R_unvax_list.append(float(nr_R_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)

        print("nr_vaxed_agegroup_untilthen (AFTER CLEANUP): " + str(nr_vaxed_agegroup_untilthen))
        print("nr_unvaxed_agegroup_untilthen (AFTER CLEANUP): " + str(nr_unvaxed_agegroup_untilthen))
        print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))
        
        print("nr_deaths_vax (AFTER CLEANUP): " + str(nr_deaths_vax))
        print("nr_deaths_novax (AFTER CLEANUP): " + str(nr_deaths_novax))

        print()
       
        perc_deaths_vax = float(nr_deaths_vax)/float(nr_vaxed_agegroup_untilthen) * 100000.0
        perc_deaths_novax = float(nr_deaths_novax)/float(nr_unvaxed_agegroup_untilthen) * 100000.0

        nr_unvaxed_agegroup_untilthen -= nr_deaths_novax
        nr_vaxed_agegroup_untilthen -= nr_deaths_vax

        nr_deaths_vax_list.append(nr_deaths_vax)
        nr_deaths_novax_list.append(nr_deaths_novax)

        perc_deaths_vax_list.append(perc_deaths_vax)
        perc_deaths_novax_list.append(perc_deaths_novax)


        weeknr_list.append(weeknr)
        weeknr += 1
        date_from = date_from + timedelta(weeks = 1)
        date_to = date_from + timedelta(weeks = 1)
        year_prev = year
        year = date_to.year



    plt.plot(weeknr_list,nr_vax1_list, color = 'b', lw=3, linestyle='solid', label='vax (1/2) administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax2_list, label='vax 2 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax3_list, label='vax 3 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax4_list, label='vax 4 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax5_list, label='vax 5 administered (/' + str(vaxnormfactor) +')')

    plt.plot(weeknr_list,perc_deaths_all_list, color = 'r', lw=3, linestyle='dotted', label='deaths all (per 100000)')
    plt.plot(weeknr_list,perc_deaths_vax_list, color = 'r', linestyle='solid', label='deaths vaxed (per 100000)')
    plt.plot(weeknr_list,perc_deaths_novax_list, color = 'r', linestyle='dashed', label='deaths not-vaxed (per 100000)')
    # plt.plot(weeknr_list,perc_deaths_unknown_list, color = 'r', linestyle='dashdot', label='deaths UNKNOWN-vaxstatus (per 100000)')
    
    # plt.plot(weeknr_list,perc_5_all_list, color = 'k', linestyle='dotted', label='deaths DOODOORZ-UNKNOWN all (per 100000)')

    plt.plot(weeknr_list,perc_U_vax_list, color = 'g', linestyle='solid', label='deaths U vaxed (per 100000)')
    plt.plot(weeknr_list,perc_G_vax_list, color = 'k', linestyle='solid', label='deaths J vaxed (per 100000)')
    plt.plot(weeknr_list,perc_I_vax_list, color = 'm', linestyle='solid', label='deaths I vaxed (per 100000)')
    # plt.plot(weeknr_list,perc_R_vax_list, color = 'c', linestyle='solid', label='deaths R vaxed (per 100000)')
    plt.plot(weeknr_list,perc_C_vax_list, color = 'c', linestyle='solid', label='deaths C vaxed (per 100000)')
    # plt.plot(weeknr_list,perc_5_vax_list, color = 'k', linestyle='solid', label='deaths DOODOORZ-UNKNOWN vaxed (per 100000)')

    plt.plot(weeknr_list,perc_U_unvax_list, color = 'g', linestyle='dashed', label='deaths U unvaxed (per 100000)')
    plt.plot(weeknr_list,perc_G_unvax_list, color = 'k', linestyle='dashed', label='deaths J unvaxed (per 100000)')
    plt.plot(weeknr_list,perc_I_unvax_list, color = 'm', linestyle='dashed', label='deaths I unvaxed (per 100000)')
    # plt.plot(weeknr_list,perc_R_unvax_list, color = 'c', linestyle='dashed', label='deaths R unvaxed (per 100000)')
    plt.plot(weeknr_list,perc_C_unvax_list, color = 'c', linestyle='dashed', label='deaths C unvaxed (per 100000)')
    # plt.plot(weeknr_list,perc_5_unvax_list, color = 'k', linestyle='dashed', label='deaths DOODOORZ-UNKNOWN unvaxed (per 100000)')

    # plt.plot(weeknr_list,perc_1_vax_list, label='deaths U (C19) vaxed')
    # plt.plot(weeknr_list,perc_2_vax_list, label='deaths I (heart) vaxed')
    # plt.plot(weeknr_list,perc_3_vax_list, label='deaths C/D (cancer/immunocompr) vaxed')
    # plt.plot(weeknr_list,perc_4_vax_list, label='deaths G (stroke/brain) vaxed')
    # plt.plot(weeknr_list,perc_1_unvax_list, label='deaths U (C19) unvaxed')
    # plt.plot(weeknr_list,perc_2_unvax_list, label='deaths I (heart) unvaxed')
    # plt.plot(weeknr_list,perc_3_unvax_list, label='deaths C/D (cancer/immunocompr) unvaxed')
    # plt.plot(weeknr_list,perc_4_unvax_list, label='deaths G (stroke/brain) unvaxed')

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    # plt.hist([dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)

    # plt.ylim(-1,1)
    plt.grid()
    plt.xlabel('week number')
    plt.ylabel('number')
    # plt.tick_params(labelright=True)
    # plt.ylabel('perc. dead in age group')
    plt.xticks(range(0, 52*nr_years + 2, 52))
    plt.subplots_adjust(bottom=0.2)
    plt.legend(bbox_to_anchor=(0.5,-0.1), loc='upper center', ncol=3)
    # plt.legend()
    plt.title("Deaths in age group " + str(age_from) +"-" + str(age_to) +", " + yearsstr + ", NL")
    
    plt.savefig("H:/data/output/plots/deaths_MY_ExU_splitcond_" + yearsstr + "_" + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    # plt.savefig("H:/data/plots/hist_deaths_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 