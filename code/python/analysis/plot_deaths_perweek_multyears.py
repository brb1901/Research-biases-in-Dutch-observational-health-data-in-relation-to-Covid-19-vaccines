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

    # for year in [2018, 2019, 2020, 2021, 2022]:
    year = 2021 # 2018
    year_tostop = 2023
    # 
    yearsstr = "2021, 2022"
    year_prev = year - 1
    
    # print(yearstr)

    age_from = 40 # 65 # 10 # 15 # 60 50
    age_to = 65 # 125 # 50 # 45 # 90 75 

    vaxnormfactor = 4000 # 8000 100000

    versionstr = "_v3"

    date_from = date(year,1,1)
    date_to = date_from + timedelta(weeks = 1)

    weeknr = 1
    nr_deaths_list = []
    nr_deaths_vax_list = []
    nr_deaths_novax_list = []
    perc_deaths_vax_list = []
    perc_deaths_novax_list = []
    perc_deaths_all_list = []
    nr_vax1_list = []
    nr_vax2_list = []
    nr_vax3_list = []
    nr_vax4_list = []
    nr_vax5_list = []
    weeknr_list = []
    while year<year_tostop: # and weeknr <=6:
        if year > year_prev:
            yearstr = str(year)
            print(year)
            filename_core = "GBAPERSOON" + yearstr + "_presentalivethatwholeyear"
            print("reading " + filename_core + " feather data")
            df_p = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core + ".ftr")
            #DEBUG Would be better to use geboortejaar!? Minder gedoe met veranderende leeftijd in een jaar, en vergelijking
            # met GBA gegevens in een vorig jaar en zo
            # nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=(age_from-1)) & (df_p['leeftijd_in_ditjaar']<(age_to-1)) ] )
            nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=(age_from)) & (df_p['leeftijd_in_ditjaar']<(age_to)) ] )
            print("Number of people alive and present in this age group end of the year: " + str(nr_p_ag))

            df_fo = df_o[ (df_o["jaar_overlijden"] == year) & 
                        (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]
            nr_deaths_all_year = len(df_fo)
            print("Number of deaths in this age group in this year: " + str(nr_deaths_all_year))
            nr_p_ag += nr_deaths_all_year
            print("Number of people in this age group in this year: " + str(nr_p_ag))

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

        # who has received a vaccination before the end of this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < (date_to)) &  #  - timedelta(weeks = 2)
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
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
        
        print("nr_deaths_vax: " + str(nr_deaths_vax))
        print("nr_deaths_novax: " + str(nr_deaths_novax))
        print("nr_deaths_all: " + str(nr_deaths_all))
        print()
       
        perc_deaths_novax = float(nr_deaths_novax)/float(nr_unvaxed_agegroup_untilthen) * 100000.0

        perc_deaths_all = float(nr_deaths_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100000.0
        perc_deaths_all_list.append(perc_deaths_all)

        nr_unvaxed_agegroup_untilthen -= nr_deaths_novax
        nr_vaxed_agegroup_untilthen -= nr_deaths_vax

        nr_deaths_vax_list.append(nr_deaths_vax)
        nr_deaths_novax_list.append(nr_deaths_novax)

        perc_deaths_vax_list.append(perc_deaths_vax)
        perc_deaths_novax_list.append(perc_deaths_novax)

        # who has received a SECOND vaccination IN this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == 2) ]
        # nr_vaxed_agegroup_thisweek = len(df_fc) 
        nr_vaxed_agegroup_thisweek = df_fc["RINPERSOON"].nunique()
        nr_vax2_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0
        # who has received a THIRD vaccination IN this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == 3) ]
        # nr_vaxed_agegroup_thisweek = len(df_fc) 
        nr_vaxed_agegroup_thisweek = df_fc["RINPERSOON"].nunique()
        nr_vax3_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0    2000.0

        # who has received a FOURTH vaccination IN this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == 4) ]
        # nr_vaxed_agegroup_thisweek = len(df_fc) 
        nr_vaxed_agegroup_thisweek = df_fc["RINPERSOON"].nunique()
        nr_vax4_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0
        # who has received a FIFTH vaccination IN this week, and is in that age group?
        df_fc = df_cims[ (df_cims["datetimeobj_prik"] < date_to) & (df_cims["datetimeobj_prik"] >= date_from) &
                         (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == 5) ]
        # nr_vaxed_agegroup_thisweek = len(df_fc) 
        nr_vaxed_agegroup_thisweek = df_fc["RINPERSOON"].nunique()
        nr_vax5_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)

        weeknr_list.append(weeknr)
        weeknr += 1
        date_from = date_from + timedelta(weeks = 1)
        date_to = date_from + timedelta(weeks = 1)
        year_prev = year
        year = date_to.year

    # plt.plot(weeknr_list,nr_deaths_vax_list, marker = 'o', label='deaths vaxed')
    # plt.plot(weeknr_list,nr_deaths_novax_list, marker = '+', label='deaths not-vaxed')
    # plt.plot(weeknr_list,nr_deaths_list, marker = 'x', label='deaths total')
    plt.plot(weeknr_list,nr_vax1_list, label='vax 1 administered (/' + str(vaxnormfactor) +')')
    plt.plot(weeknr_list,nr_vax2_list, label='vax 2 administered (/' + str(vaxnormfactor) +')')
    plt.plot(weeknr_list,nr_vax3_list, label='vax 3 administered (/' + str(vaxnormfactor) +')')
    plt.plot(weeknr_list,nr_vax4_list, label='vax 4 administered (/' + str(vaxnormfactor) +')')
    plt.plot(weeknr_list,nr_vax5_list, label='vax 5 administered (/' + str(vaxnormfactor) +')')
    plt.plot(weeknr_list,perc_deaths_vax_list, label='deaths vaxed (per 100000)')
    plt.plot(weeknr_list,perc_deaths_novax_list, label='deaths not-vaxed (per 100000)')
    plt.plot(weeknr_list,perc_deaths_all_list, label='deaths all (per 100000)')

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    # plt.hist([dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)
    plt.xlabel('week number')
    plt.ylabel('number')
    # plt.ylabel('perc. dead in age group')
    # plt.xticks(range(1,52,5))
    plt.legend()
    plt.title("Deaths in age group " + str(age_from) +"-" + str(age_to) +", " + yearsstr + ", NL")
    
    plt.savefig("H:/data/plots/deaths_vaccines_" + yearsstr + "_" + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    # plt.savefig("H:/data/plots/hist_deaths_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 