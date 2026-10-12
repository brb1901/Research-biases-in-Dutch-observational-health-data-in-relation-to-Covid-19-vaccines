import pandas as pd
import time
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt


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

    print("reading GBAPERSOON_trackable_years2018-2022_ext feather data")
    df_p = pd.read_feather(basepath+"python_pandas/GBA/"+"GBAPERSOON_trackable_years2018-2022_ext.ftr")

    filename_core = "DOODOORZ2015-2022" 
    print("reading " + filename_core + " feather data")
    df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")

    # for year in [2018, 2019, 2020, 2021, 2022]:
    year = 2020 # 2019 # 2018 2021 # 
    year_tostop = 2023 #2022 #  
    nr_years = year_tostop - year
    # 
    yearsstr = "2020-2022" # "2021" #"2019-2022" # 
    year_prev = year - 1
    
    print("First year:")
    print(year)

    # age_from = 70 # 50 # 15 # 65 # 10 # 15 # 60 50 40 # 
    # age_to = 125 # 65 # 50 # 125 # 50 # 45 # 90 75 65 # 

    birthyear_from = 1990 # 1970 # 1950 # 1900 #year - age_to
    birthyear_to = 2010 #1990 # 1970 # 1950 #year - age_from

    age_from = year - birthyear_to
    age_to = year - birthyear_from

    df_p = df_p[ (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to)  ] # &  ((df_p['jaar_overlijden']>=year) | (df_p['jaar_overlijden']==-1))
    nr_p_ag = len( df_p )
    # nr_p_ag_all = nr_p_ag
    print("Number of people alive and present in this age group start of the year: " + str(nr_p_ag))
    df_p_test = df_p[ (df_p['jaar_overlijden']==year)  ]
    print("Number of people in this age group who died this year : " + str(len(df_p_test))) # or later

    # Select only CIMS entries who are in our trackable list and in the right age group
    df_cims = df_cims[  (df_cims['RINPERSOON'].isin(df_p['RINPERSOON']))  ]

    # Select only DODEN entries who are in our trackable list and in the right age group
    df_o = df_o[df_o['RINPERSOON'].isin(df_p['RINPERSOON'])]

    # print(df_p.head(10))

    vaxnormfactor = 300000 # 4000: 1900-1950; 40000: 1950-1970; 100000: 1970-1990; 300000: 1990-2010

    weeksteps = 4

    versionstr = "_v1"

    date_from = date(year,1,1)
    date_to = date_from + timedelta(weeks = weeksteps)

    weeknr = 1
    nr_deaths_list = []
    nr_deaths_vax_list = []
    nr_deaths_novax_list = []
    perc_deaths_vax_list = []
    perc_deaths_novax_list = []
    perc_deaths_all_list = []
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
    perc_U_unvax_list = []
    perc_I_unvax_list = []
    perc_C_unvax_list = []
    perc_G_unvax_list = []

    while year<year_tostop: # and weeknr <=6:
        if year > year_prev:
            yearstr = str(year)
            print(year)

            # filename_core = "DOODOORZ" + yearstr 
            # print("reading " + filename_core + " feather data")
            # df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")
            # print("Number of DOODOORZ: " + str(len(df_do)))
            # # df_do = df_do[df_do['RINPERSOON'].isin(df_p['RINPERSOON'])]
            # # print("Number of trackable DOODOORZ: " + str(len(df_do)))

            df_fo = df_o[ (df_o["jaar_overlijden"] == year)  ] # year &  (df_o['RINPERSOON'].isin(df_p['RINPERSOON']))
            nr_deaths_all_year = len(df_fo)
            print("Number of trackable deaths in this age group in this year: " + str(nr_deaths_all_year))

            df_fo = df_fo[df_fo['RINPERSOON'].isin(df_do['RINPERSOON'])] # year &  (df_o['RINPERSOON'].isin(df_p['RINPERSOON']))
            nr_deaths_all_year = len(df_fo)
            print("Number of deaths in this age group in this year after selecting deaths with DOODOORZ: " + str(nr_deaths_all_year))

            #DEBUG: DOUBLE CHECK
            df_fo = df_fo[df_fo['RINPERSOON'].isin(df_p['RINPERSOON'])] # year &  (df_o['RINPERSOON'].isin(df_p['RINPERSOON']))
            nr_deaths_all_year = len(df_fo)
            print("Number of deaths in this age group in this year after (again) selecting trackable: " + str(nr_deaths_all_year))

            # nr_p_ag += nr_deaths_all_year
            # print("Number of people in this age group in this year: " + str(nr_p_ag))

            # who has received a vaccination before the start of this period, and is in that age group?
            df_fc = df_cims[ (df_cims["datetimeobj_prik"] < (date_from)) &  #  - timedelta(weeks = 2)                                
                                (df_cims["prik_nummer"] == 1) ]           
            nr_vaxed_agegroup_untilthen = df_fc['RINPERSOON'].nunique()
            nr_unvaxed_agegroup_untilthen = nr_p_ag - nr_vaxed_agegroup_untilthen
            print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup_untilthen))
            print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup_untilthen))
            print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))

            

        print(weeknr)
        print(date_from)
        # print("selecting deaths in " + yearstr)
        df_fo = df_o[ (df_o["datetimeobj_overlijden"] >= date_from) & (df_o["datetimeobj_overlijden"] < date_to) ]
        df_fo = df_fo[ (df_fo['RINPERSOON'].isin(df_p['RINPERSOON'])) ]
        # nr_deaths_all = len(df_fo)
        nr_deaths_all = df_fo['RINPERSOON'].nunique()
        nr_deaths_list.append(nr_deaths_all)

        # nr_vaxed_agegroup_untilthen = len(df_fc)        
        
        # who has received a FIRST vaccination IN this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["prik_nummer"] == 1) ]
        # nr_vaxed_agegroup_thisweek = len(df_fc) 
        nr_vaxed_agegroup_thisweek = df_fc['RINPERSOON'].nunique()
        nr_vaxed_agegroup_untilthen += nr_vaxed_agegroup_thisweek
        if nr_vaxed_agegroup_untilthen==0:
            nr_vaxed_agegroup_untilthen=1

        # who has received a vaccination before the end of this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < (date_to)) &  #  - timedelta(weeks = 2)
                         (df_cims["prik_nummer"] == 1) ]

        # select those deaths that we can also find in CIMS, vaccinations only before the end of this week
        df_ovax = df_fo[df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]
        # df['Rinpersoon'].nunique()
        # nr_deaths_vax = len(df_ovax)
        nr_deaths_vax = df_ovax['RINPERSOON'].nunique()
        perc_deaths_vax = float(nr_deaths_vax)/float(nr_vaxed_agegroup_untilthen) * 100000.0
    
        nr_unvaxed_agegroup_untilthen = nr_unvaxed_agegroup_untilthen - nr_vaxed_agegroup_thisweek
        nr_vax1_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0  100000.0
        nr_deaths_novax = nr_deaths_all - nr_deaths_vax
        print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup_untilthen))
        print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup_untilthen))
        print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))
        perc_vaxed = 100.0 * float(nr_vaxed_agegroup_untilthen)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen ) # nr_p_ag
        print("perc_vaxed until then (surviving only): " + str(perc_vaxed))
        
        print("nr_deaths_vax: " + str(nr_deaths_vax))
        print("nr_deaths_novax: " + str(nr_deaths_novax))
        print("nr_deaths_all: " + str(nr_deaths_all))

        # select those vaccinated deaths that we can find in DOODOORZ
        df_do_vax = df_do[df_do['RINPERSOON'].isin(df_ovax['RINPERSOON'])]
        nr_U_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('U')] ) # Covid and similar
        nr_I_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('I')] ) # heart diseases
        # nr_C_ICD10 = len( df_do_vax[ (df_do_vax['UCCODE'].str.startswith('C')) | (df_do_vax['UCCODE'].str.startswith('D')) ] ) # cancer, immunodeficiencies
        nr_C_ICD10 = len( df_do_vax[ (df_do_vax['UCCODE'].str.startswith('X')) | (df_do_vax['UCCODE'].str.startswith('Y')) ] ) # external, self-harm, accidents, harmed by others
        # nr_G_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('G')] ) # strokes, brain things
        nr_G_ICD10 = len( df_do_vax[df_do_vax['UCCODE'].str.startswith('R')] ) # rest category, sudden deaths
        print("Vaccinated: found in DOODOORZ: " + str(len(df_do_vax)))
        # print("Vaccinated: nr_U_ICD10: " + str(nr_U_ICD10))
        # print("Vaccinated: nr_I_ICD10: " + str(nr_I_ICD10))
        print("Vaccinated: nr_U_ICD10 per 100000: " + str(float(nr_U_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0))
        print("Vaccinated: nr_I_ICD10 per 100000: " + str(float(nr_I_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0))
        print("Vaccinated: nr_C_ICD10 per 100000: " + str(float(nr_C_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0))
        print("Vaccinated: nr_G_ICD10 per 100000: " + str(float(nr_G_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0))
        #DEBUG
        df_vax_bad = df_ovax[~df_ovax['RINPERSOON'].isin(df_do['RINPERSOON'])]
        print("Vaccinated: NOT found in DOODOORZ: " + str(len(df_vax_bad)))

        # nr_heartdeaths_vax = nr_I_ICD10

        perc_U_vax_list.append(float(nr_U_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_I_vax_list.append(float(nr_I_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_C_vax_list.append(float(nr_C_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)
        perc_G_vax_list.append(float(nr_G_ICD10)/float(nr_vaxed_agegroup_untilthen) * 100000.0)

        #DEBUG!!:
        # perc_U_vax_list.append(float(nr_U_ICD10))
        # perc_I_vax_list.append(float(nr_I_ICD10))
        # perc_C_vax_list.append(float(nr_C_ICD10))
        # perc_G_vax_list.append(float(nr_G_ICD10))

        # select those UNvaccinated deaths that we can find in DOODOORZ
        df_onovax = df_fo[~df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]

        df_do_novax = df_do[df_do['RINPERSOON'].isin(df_onovax['RINPERSOON'])]
        nr_U_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('U')] )
        nr_I_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('I')] )
        # nr_C_ICD10 = len( df_do_novax[ (df_do_novax['UCCODE'].str.startswith('C')) | (df_do_novax['UCCODE'].str.startswith('D')) ] ) # cancer, immunodeficiencies
        nr_C_ICD10 = len( df_do_novax[ (df_do_novax['UCCODE'].str.startswith('X')) | (df_do_novax['UCCODE'].str.startswith('Y')) ] ) # external, self-harm, accidents, harmed by others
        # nr_G_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('G')] )
        nr_G_ICD10 = len( df_do_novax[df_do_novax['UCCODE'].str.startswith('R')] ) # rest category, sudden deaths
        print("Unvaccinated: found in DOODOORZ: " + str(len(df_onovax)))
        # print("Unvaccinated: nr_U_ICD10: " + str(nr_U_ICD10))
        # print("Unvaccinated: nr_I_ICD10: " + str(nr_I_ICD10))
        print("Unvaccinated: nr_U_ICD10 per 100000: " + str(float(nr_U_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0))
        print("Unvaccinated: nr_I_ICD10 per 100000: " + str(float(nr_I_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0))
        print("Unvaccinated: nr_C_ICD10 per 100000: " + str(float(nr_C_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0))
        print("Unvaccinated: nr_G_ICD10 per 100000: " + str(float(nr_G_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0))
        #DEBUG
        df_novax_bad = df_onovax[~df_onovax['RINPERSOON'].isin(df_do['RINPERSOON'])]
        print("Unvaccinated: NOT found in DOODOORZ: " + str(len(df_novax_bad)))

        # nr_heartdeaths_novax = nr_I_ICD10

        perc_U_unvax_list.append(float(nr_U_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_I_unvax_list.append(float(nr_I_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_C_unvax_list.append(float(nr_C_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)
        perc_G_unvax_list.append(float(nr_G_ICD10)/float(nr_unvaxed_agegroup_untilthen) * 100000.0)

        #DEBUG!!:
        # perc_U_unvax_list.append(float(nr_U_ICD10))
        # perc_I_unvax_list.append(float(nr_I_ICD10))
        # perc_C_unvax_list.append(float(nr_C_ICD10))
        # perc_G_unvax_list.append(float(nr_G_ICD10))

        print()
       
        perc_deaths_novax = float(nr_deaths_novax)/float(nr_unvaxed_agegroup_untilthen) * 100000.0

        perc_deaths_all = float(nr_deaths_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100000.0
        ##DEBUG!!: now only HEART deaths in all!!
        # perc_deaths_all = float(nr_heartdeaths_vax + nr_heartdeaths_novax)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100000.0
        perc_deaths_all_list.append(perc_deaths_all)

        nr_unvaxed_agegroup_untilthen -= nr_deaths_novax
        nr_vaxed_agegroup_untilthen -= nr_deaths_vax

        nr_deaths_vax_list.append(nr_deaths_vax)
        nr_deaths_novax_list.append(nr_deaths_novax)

        perc_deaths_vax_list.append(perc_deaths_vax)
        perc_deaths_novax_list.append(perc_deaths_novax)

        # # who has received a SECOND vaccination IN this week, and is in that age group?
        # df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
        #                  (df_cims["prik_nummer"] == 2) ]
        # # nr_vaxed_agegroup_thisweek = len(df_fc) 
        # nr_vaxed_agegroup_thisweek = df_fc['RINPERSOON'].nunique()
        # nr_vax2_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0

        # # who has received a THIRD vaccination IN this week, and is in that age group?
        # df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
        #                  (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
        #                  (df_cims["prik_nummer"] == 3) ]
        # # nr_vaxed_agegroup_thisweek = len(df_fc) 
        # nr_vaxed_agegroup_thisweek = df_fc['RINPERSOON'].nunique()
        # nr_vax3_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0    2000.0

        # # who has received a FOURTH vaccination IN this week, and is in that age group?
        # df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
        #                  (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
        #                  (df_cims["prik_nummer"] == 4) ]
        # # nr_vaxed_agegroup_thisweek = len(df_fc) 
        # nr_vaxed_agegroup_thisweek = df_fc['RINPERSOON'].nunique()
        # nr_vax4_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0
        # # who has received a FIFTH vaccination IN this week, and is in that age group?
        # df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
        #                  (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
        #                  (df_cims["prik_nummer"] == 5) ]
        # # nr_vaxed_agegroup_thisweek = len(df_fc) 
        # nr_vaxed_agegroup_thisweek = df_fc['RINPERSOON'].nunique()
        # nr_vax5_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)

        weeknr_list.append(weeknr)
        weeknr += weeksteps
        date_from = date_from + timedelta(weeks = weeksteps)
        date_to = date_from + timedelta(weeks = weeksteps)
        year_prev = year
        year = date_to.year

    # plt.plot(weeknr_list,nr_deaths_vax_list, label='deaths vaxed')
    # plt.plot(weeknr_list,nr_deaths_novax_list, label='deaths not-vaxed')
    # plt.plot(weeknr_list,nr_deaths_list, label='deaths total')

    plt.plot(weeknr_list,nr_vax1_list, color = 'b', lw=3, linestyle='solid', label='vax 1 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax2_list, label='vax 2 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax3_list, label='vax 3 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax4_list, label='vax 4 administered (/' + str(vaxnormfactor) +')')
    # plt.plot(weeknr_list,nr_vax5_list, label='vax 5 administered (/' + str(vaxnormfactor) +')')

    plt.plot(weeknr_list,perc_deaths_vax_list, color = 'r', linestyle='solid', label='deaths vaxed (per 100000)')
    plt.plot(weeknr_list,perc_deaths_novax_list, color = 'r', linestyle='dashed', label='deaths not-vaxed (per 100000)')
    plt.plot(weeknr_list,perc_deaths_all_list, color = 'r', lw=3, linestyle='dotted', label='deaths all (per 100000)')

    plt.plot(weeknr_list,perc_U_vax_list, color = 'g', linestyle='solid', label='deaths U (C19) vaxed (per 100000)')
    plt.plot(weeknr_list,perc_I_vax_list, color = 'm', linestyle='solid', label='deaths I (heart) vaxed (per 100000)')
    # plt.plot(weeknr_list,perc_C_vax_list, color = 'c', linestyle='solid', label='deaths C/D (cancer/immunocompr) vaxed (per 100000)')
    # plt.plot(weeknr_list,perc_G_vax_list, color = 'k', linestyle='solid', label='deaths G (stroke/brain) vaxed (per 100000)')
    plt.plot(weeknr_list,perc_C_vax_list, color = 'c', linestyle='solid', label='deaths X/Y (external) vaxed (per 100000)')
    plt.plot(weeknr_list,perc_G_vax_list, color = 'k', linestyle='solid', label='deaths R (rest/unexplained) vaxed (per 100000)')

    plt.plot(weeknr_list,perc_U_unvax_list, color = 'g', linestyle='dashed', label='deaths U (C19) unvaxed (per 100000)')
    plt.plot(weeknr_list,perc_I_unvax_list, color = 'm', linestyle='dashed', label='deaths I (heart) unvaxed (per 100000)')
    # plt.plot(weeknr_list,perc_C_unvax_list, color = 'c', linestyle='dashed', label='deaths C/D (cancer/immunocompr) unvaxed (per 100000)')
    # plt.plot(weeknr_list,perc_G_unvax_list, color = 'k', linestyle='dashed', label='deaths G (stroke/brain) unvaxed (per 100000)')
    plt.plot(weeknr_list,perc_C_unvax_list, color = 'c', linestyle='dashed', label='deaths X/Y (external) unvaxed (per 100000)')
    plt.plot(weeknr_list,perc_G_unvax_list, color = 'k', linestyle='dashed', label='deaths R (rest/unexplained) unvaxed (per 100000)')

    # plt.plot(weeknr_list,perc_U_vax_list, label='deaths U (C19) vaxed')
    # plt.plot(weeknr_list,perc_I_vax_list, label='deaths I (heart) vaxed')
    # plt.plot(weeknr_list,perc_C_vax_list, label='deaths C/D (cancer/immunocompr) vaxed')
    # plt.plot(weeknr_list,perc_G_vax_list, label='deaths G (stroke/brain) vaxed')
    # plt.plot(weeknr_list,perc_U_unvax_list, label='deaths U (C19) unvaxed')
    # plt.plot(weeknr_list,perc_I_unvax_list, label='deaths I (heart) unvaxed')
    # plt.plot(weeknr_list,perc_C_unvax_list, label='deaths C/D (cancer/immunocompr) unvaxed')
    # plt.plot(weeknr_list,perc_G_unvax_list, label='deaths G (stroke/brain) unvaxed')

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    # plt.hist([dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)
    plt.xlabel('week number')
    plt.ylabel('number')
    # plt.ylabel('perc. dead in age group')
    # plt.xticks(range(1,52,5))
    # plt.subplots_adjust(right=0.75)
    # plt.legend(bbox_to_anchor=(1.05,1.0), loc='upper left')
    plt.xticks(range(0, 52*nr_years + 2, 52))
    plt.subplots_adjust(bottom=0.2)
    plt.legend(bbox_to_anchor=(0.5,-0.1), loc='upper center', ncol=3)
    # plt.legend()
    plt.title("Deaths in age group " + str(birthyear_from) +"-" + str(birthyear_to) +", " + yearsstr + ", NL")
    
    plt.savefig("H:/data/output/plots/deaths_numbers_trackable_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    # plt.savefig("H:/data/plots/hist_deaths_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 