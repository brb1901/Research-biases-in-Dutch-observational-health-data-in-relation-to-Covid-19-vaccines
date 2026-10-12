import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import date, datetime, timedelta
import time


def calc_diagnoses_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, versionstr, booster=False):
    # basepath = "H:/data/"
    year = 2018 # 2021 # 2019 # 2018 2021 # 
    firstyear = year
    year_tostop = 2022 #  2024 #
    nr_years = year_tostop - year

    # min_nr_vaxed = 100
    # 
    yearsstr = "2018-2021" #  "2021" #"2019-2022" # "2021-2023" #
    year_prev = year - 1

    shortlyafter_weeks = 8
    shortlybefore_weeks = 8
    
    print("First year:")
    print(year)

    # age_from = refyear - birthyear_to
    # age_to = refyear - birthyear_from
    # filename_core = "diagnosis_baseline_" + str(age_from) + "_" + str(age_to) + "_v0"
    # filename_ftr = basepath+"python_pandas/diagnosis_baselines/"+filename_core+".ftr"
    # df_db = pd.read_feather(filename_ftr) # baseline diagnosis for this age group!

    # age_from = 70 # 50 # 15 # 65 # 10 # 15 # 60 50 40 # 
    # age_to = 125 # 65 # 50 # 125 # 50 # 45 # 90 75 65 # 

    # df_p = df_p[ (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) & 
    #              (df_p['WLZ_bit']==wlz_bit) ] # &  ((df_p['jaar_overlijden']>=year) | (df_p['jaar_overlijden']==-1))
    
    if wlz_bit==0 or wlz_bit==-1:
        if med_rxrisk_scores==0:
            print("HEALTHY SUBGROUP: DEBUG: df_p = df_p[ (df_p'med_rxrisk_score_weightedpratt_prevyear_bin']==0) ]")
            df_p = df_p[ (df_p["med_rxrisk_score_weightedpratt_prevyear_bin"]==0) ]
        elif med_rxrisk_scores==1:
            print("UNHEALTHY SUBGROUP: DEBUG: df_p = df_p[ (df_p'med_rxrisk_score_weightedpratt_prevyear_bin']>0) ]")
            df_p = df_p[ (df_p["med_rxrisk_score_weightedpratt_prevyear_bin"]>0) ]
        # else: if med_rxrisk_scores is -1 (or anything other than 0 or 1), then just all med_rxrisk_scores!
    else:
        if wlz_levels==0:
            print("HEALTHY SUBGROUP: DEBUG: df_p = df_p[ (df_p['WLZ_level']<=3) ]")
            df_p = df_p[ (df_p["WLZ_level"]<=3) ]
        elif wlz_levels==1:
            print("UNHEALTHY SUBGROUP: DEBUG: df_p = df_p[ (df_p['WLZ_level]>3) ]")
            df_p = df_p[ (df_p["WLZ_level"]>3) ]
        # else: if wlz_levels is -1 (or anything other than 0 or 1), then just all wlz_levels!

    nr_p_ag = len( df_p )
    # nr_p_ag_all = nr_p_ag
    print("Number of people alive and present in this age group start of processing: " + str(nr_p_ag))
    # df_p_test = df_p[ (df_p['year_dead']==year)  ]
    # print("Number of people in this age group who died this year : " + str(len(df_p_test))) 

    if nr_p_ag==0:
        print("Number of people alive and present in this age group is zero! Ending this analysis for this group")
    else:
    # print(df_p.head(10))
    # versionstr = "_v1"

        date_from = date(year,1,1)
        date_to = date_from + timedelta(weeks = weeksteps)

        weeknr = 0 + weeksteps
        nr_diagnosis_list = []
        nr_diagnosis_vax_list = []
        nr_diagnosis_novax_list = []
        perc_diagnosis_vax_list = []
        perc_diagnosis_novax_list = []
        perc_diagnosis_all_list = []
        nr_vax1_list = []

        # perc_diagnosis_vax_covid_list = []
        # perc_diagnosis_vax_noncovid_list = []
        # perc_diagnosis_novax_covid_list = []
        # perc_diagnosis_novax_noncovid_list = []

        perc_vaccinated_list = []

        # perc_diagnosis_covid_list = []
        # nr_diagnosis_covid_list = []

        # nr_diagnosis_vax_list = []
        # nr_diagnosis_novax_list = []
        nr_vaxed_alive_list = []
        nr_unvaxed_alive_list = []

        nr_vax2_list = []
        nr_vax3_list = []
        # nr_vax4_list = []
        # nr_vax5_list = []
        weeknr_list = []

        # perc_diagnosis_baseline_list = []
        # nr_diagnosis_baseline_list = []

        nr_deaths_afterdiag_all_list = []
        nr_deaths_afterdiag_vaxed_list = []
        nr_deaths_afterdiag_unvaxed_list = []
        perc_deaths_afterdiag_all_list = []
        perc_deaths_afterdiag_vax_list = []
        perc_deaths_afterdiag_novax_list = []

        nr_infected_beforediag_all_list = []
        nr_infected_beforediag_vaxed_list = []
        nr_infected_beforediag_unvaxed_list = []
        perc_infected_beforediag_all_list = []
        perc_infected_beforediag_vax_list = []
        perc_infected_beforediag_novax_list = []

        nr_vaxed_agegroup_untilthen = 0
        nr_vaxed_agegroup_untilthen_incldead = 0
        nr_unvaxed_agegroup_untilthen = nr_p_ag - nr_vaxed_agegroup_untilthen

        perc_diagnosis_maxval = -1.0
        perc_diagnosis_minval = 101.0
        perc_deathinf_maxval = -1.0
        perc_deathinf_minval = 101.0
        nr_diagnosis_total = 0
        nr_deaths_total = 0

        nr_periods = 52/weeksteps
        nr_diag_oneyear = 0
        nr_weeks_thisyear = 0
        nr_diag_thisyear_avg_list = []

        while year<year_tostop: # and weeknr <=6:
            if year > year_prev:
                yearstr = str(year)
                print(year)
                # i_year_predict = year-refyear
                # print(i_year_predict)

                print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup_untilthen))
                print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup_untilthen))
                print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))

                if year>firstyear:
                    nr_diag_thisyear_avg = float(nr_diag_oneyear)/float(nr_periods)
                    for j in range(nr_weeks_thisyear):
                        nr_diag_thisyear_avg_list.append(nr_diag_thisyear_avg)
                    nr_weeks_thisyear = 0
                    nr_diag_oneyear = 0

            print(weeknr)
            print(date_from)
            print(date_to)
            week_nr_thisyear = date_to.isocalendar().week
            # year_derived = date_to.isocalendar().year
            month = date_to.month
            if month==12 and (week_nr_thisyear==1 or week_nr_thisyear==53):
                week_nr_thisyear = 52
            print(week_nr_thisyear)
            # print("selecting diagnosis in " + yearstr)

            # Who had the diagnosis in this period?    # (df_p["year_diagnosis"] == year) & 
            df_pd = df_p[ ( (df_p[yearstr+"_"+"week1nr"] <= week_nr_thisyear) & (df_p[yearstr+"_"+"week1nr"] > (week_nr_thisyear-weeksteps)) |
                            (df_p[yearstr+"_"+"week2nr"] <= week_nr_thisyear) & (df_p[yearstr+"_"+"week2nr"] > (week_nr_thisyear-weeksteps)) |
                            (df_p[yearstr+"_"+"week3nr"] <= week_nr_thisyear) & (df_p[yearstr+"_"+"week3nr"] > (week_nr_thisyear-weeksteps)) |
                            (df_p[yearstr+"_"+"week4nr"] <= week_nr_thisyear) & (df_p[yearstr+"_"+"week4nr"] > (week_nr_thisyear-weeksteps)) ) ]
            nr_diagnosis_all = len(df_pd)
            nr_diagnosis_list.append(nr_diagnosis_all)
            nr_diagnosis_total += nr_diagnosis_all
            nr_diag_oneyear += nr_diagnosis_all

            # who has received a FIRST vaccination IN this period, and is in that age group? (dead or alive)
            if booster==False:
                df_fc = df_p[ (df_p["year_firstvax"] == year) & ((df_p["week_nr_firstvax"] <= week_nr_thisyear) & (df_p["week_nr_firstvax"] > (week_nr_thisyear-weeksteps))) ]
            else:
                df_fc = df_p[ (df_p["treatment"] == True) & (df_p["year_thirdvax"] == year) & ((df_p["week_nr_thirdvax"] <= week_nr_thisyear) & (df_p["week_nr_thirdvax"] > (week_nr_thisyear-weeksteps))) ]
            nr_vaxed_agegroup_thisweek = len(df_fc)
            print("Nr new vaccinations this period: " + str(nr_vaxed_agegroup_thisweek))

            nr_vaxed_agegroup_untilthen += nr_vaxed_agegroup_thisweek
            nr_vaxed_agegroup_untilthen_incldead += nr_vaxed_agegroup_thisweek
            if nr_vaxed_agegroup_untilthen==0: # to avoid dividing by zero, just in case
                nr_vaxed_agegroup_untilthen=1
                nr_vaxed_agegroup_untilthen_incldead=1

            # select those diagnoses in this period that are also vaccinated
            df_ovax = df_pd[df_pd["treatment"]==1 & ( ((df_pd["year_firstvax"] == year) & (df_pd["week_nr_firstvax"] <= week_nr_thisyear)) |
                                                       (df_pd["year_firstvax"] < year) )]
            # df['Rinpersoon'].nunique()
            nr_diagnosis_vax = len(df_ovax)
            # nr_diagnosis_vax = df_ovax['RINPERSOON'].nunique()
            perc_diagnosis_vax = float(nr_diagnosis_vax)/float(nr_vaxed_agegroup_untilthen) * 100.0
            if perc_diagnosis_vax > perc_diagnosis_maxval:
                perc_diagnosis_maxval = perc_diagnosis_vax
            if perc_diagnosis_vax < perc_diagnosis_minval:
                perc_diagnosis_minval = perc_diagnosis_vax

            nr_diagnosis_novax = nr_diagnosis_all - nr_diagnosis_vax

            print("nr_diagnosis_all: " + str(nr_diagnosis_all))
            print("nr_diagnosis_vax: " + str(nr_diagnosis_vax))
            print("nr_diagnosis_novax (calc INDIRECTLY from all and vaxed diagnosis data): " + str(nr_diagnosis_novax))

            # Who had the diagnosis AND also died shortly after?
            # if week_nr_thisyear>=(52-shortlyafter_weeks):
            week_nr_nextyear = week_nr_thisyear+shortlyafter_weeks-52

            df_pd_dead = df_pd[ ((df_pd["year_dead"] == year) &  (df_pd["week_nr_dead"] <= (week_nr_thisyear+shortlyafter_weeks))) | 
                                 ((df_pd["year_dead"] == (year+1)) & (df_pd["week_nr_dead"] <= week_nr_nextyear)) ]
            nr_deaths_afterdiag_all = len(df_pd_dead)

            # df_pd_dead_ovax = df_pd_dead[ df_pd_dead['RINPERSOON'].isin(df_ovax['RINPERSOON']) ]
            df_pd_dead_ovax = df_pd_dead[ df_pd_dead["treatment"]==1 & ( ((df_pd_dead["year_firstvax"] == year) & (df_pd_dead["week_nr_firstvax"] <= week_nr_thisyear)) |
                                                       (df_pd_dead["year_firstvax"] < year) )]
            # df_fo_rightsex = df_fo[ df_fo['RINPERSOON'].isin(df_pf['RINPERSOON']) ]
            # df_ovax[ ((df_ovax["year_dead"] == year) &  (df_ovax["week_nr_dead"] <= (week_nr_thisyear+shortlyafter_weeks))) | 
            #                      ((df_ovax["year_dead"] == (year+1)) & (df_ovax["week_nr_dead"] <= week_nr_nextyear)) ]            
            nr_deaths_afterdiag_vaxed = len(df_pd_dead_ovax)
            nr_deaths_afterdiag_unvaxed = nr_deaths_afterdiag_all - nr_deaths_afterdiag_vaxed

            # Who was covid-infected shortly before? 
            if year>=2020:
                week_nr_prevyear = week_nr_thisyear - shortlybefore_weeks +52
                df_pd_inf = df_p[ ((df_pd["covidinf_year1nr"] == float(year)) & (df_p["covidinf_week1nr"] <= float(week_nr_thisyear)) & (df_p["covidinf_week1nr"] > float(week_nr_thisyear-shortlybefore_weeks))) |
                                ((df_pd["covidinf_year2nr"] == float(year)) & (df_p["covidinf_week2nr"] <= float(week_nr_thisyear)) & (df_p["covidinf_week2nr"] > float(week_nr_thisyear-shortlybefore_weeks))) |
                                ((df_pd["covidinf_year3nr"] == float(year)) & (df_p["covidinf_week3nr"] <= float(week_nr_thisyear)) & (df_p["covidinf_week3nr"] > float(week_nr_thisyear-shortlybefore_weeks))) |
                                ((df_pd["covidinf_year4nr"] == float(year)) & (df_p["covidinf_week4nr"] <= float(week_nr_thisyear)) & (df_p["covidinf_week4nr"] > float(week_nr_thisyear-shortlybefore_weeks))) | 
                                ((df_pd["covidinf_year1nr"] == float(year-1)) & (df_p["covidinf_week1nr"] > float(week_nr_prevyear))) |
                                ((df_pd["covidinf_year2nr"] == float(year-1)) & (df_p["covidinf_week2nr"] > float(week_nr_prevyear))) |
                                ((df_pd["covidinf_year3nr"] == float(year-1)) & (df_p["covidinf_week3nr"] > float(week_nr_prevyear))) |
                                ((df_pd["covidinf_year4nr"] == float(year-1)) & (df_p["covidinf_week4nr"] > float(week_nr_prevyear))) ]
                                
                nr_infected_beforediag_all = len(df_pd_inf)
                # Who was covid-infected in this period AND was vaccinated? 
                # df_pd_inf_ovax = df_pd_inf[ df_pd_inf['RINPERSOON'].isin(df_ovax['RINPERSOON']) ]
                df_pd_inf_ovax = df_pd_inf[ df_pd_inf["treatment"]==1 & ( ((df_pd_inf["year_firstvax"] == year) & (df_pd_inf["week_nr_firstvax"] <= week_nr_thisyear)) |
                                                       (df_pd_inf["year_firstvax"] < year) )]
                # df_ovax[ ((df_pd["covidinf_year1nr"] == float(year)) & (df_ovax["covidinf_week1nr"] <= float(week_nr_thisyear)) & (df_ovax["covidinf_week1nr"] > float(week_nr_thisyear-weeksteps))) |
                #                   ((df_ovax["covidinf_year2nr"] == float(year)) & (df_ovax["covidinf_week2nr"] <= float(week_nr_thisyear)) & (df_ovax["covidinf_week2nr"] > float(week_nr_thisyear-weeksteps))) |
                #                   ((df_ovax["covidinf_year3nr"] == float(year)) & (df_ovax["covidinf_week3nr"] <= float(week_nr_thisyear)) & (df_ovax["covidinf_week3nr"] > float(week_nr_thisyear-weeksteps))) |
                #                   ((df_ovax["covidinf_year4nr"] == float(year)) & (df_ovax["covidinf_week4nr"] <= float(week_nr_thisyear)) & (df_ovax["covidinf_week4nr"] > float(week_nr_thisyear-weeksteps))) ]
                nr_infected_beforediag_vaxed = len(df_pd_inf_ovax)
                nr_infected_beforediag_unvaxed = nr_infected_beforediag_all - nr_infected_beforediag_vaxed
            else:
                nr_infected_beforediag_all = 0
                nr_infected_beforediag_vaxed = 0
                nr_infected_beforediag_unvaxed = 0
            
            # df_onovax = df_pd[df_pd["control"]==1]
            # nr_diagnosis_novax = len(df_onovax)
            # print("nr_diagnosis_novax (calc DIRECTLY from no-vaxed diagnosis data): " + str(nr_diagnosis_novax))

            # Who died in this period?
            df_pdead = df_p[ (df_p["year_dead"] == year) & ((df_p["week_nr_dead"] <= week_nr_thisyear) & (df_p["week_nr_dead"] > (week_nr_thisyear-weeksteps))) ]
            nr_deaths_all = len(df_pdead)
            # nr_deaths_list.append(nr_deaths_all)
            nr_deaths_total += nr_deaths_all
            # select those deaths in this period that are also vaccinated
            df_ovax = df_pdead[df_pdead["treatment"]==1]
            # df['Rinpersoon'].nunique()
            nr_deaths_vax = len(df_ovax)

            nr_deaths_novax = nr_deaths_all - nr_deaths_vax

            print("nr_deaths_all: " + str(nr_deaths_all))
            print("nr_deaths_vax: " + str(nr_deaths_vax))
            print("nr_deaths_novax (calc INDIRECTLY from all and vaxed dead data): " + str(nr_deaths_novax))
            
            df_onovax = df_pdead[df_pdead["control"]==1]
            nr_deaths_novax = len(df_onovax)
            print("nr_deaths_novax (calc DIRECTLY from no-vaxed dead data): " + str(nr_deaths_novax))
        
            nr_unvaxed_agegroup_untilthen = nr_unvaxed_agegroup_untilthen - nr_vaxed_agegroup_thisweek
            # nr_vax1_list.append(float(nr_vaxed_agegroup_thisweek)/vaxnormfactor)     # 80000.0  2000.0  100000.0
            if booster:
                df_fc_extra = df_p[ (df_p["year_firstvax"] == year) & ((df_p["week_nr_firstvax"] <= week_nr_thisyear) & (df_p["week_nr_firstvax"] > (week_nr_thisyear-weeksteps))) ]
                nr_vaxed_agegroup_thisweek_extra = len(df_fc_extra)
            else:
                nr_vaxed_agegroup_thisweek_extra = nr_vaxed_agegroup_thisweek
            nr_vax1_list.append(nr_vaxed_agegroup_thisweek_extra)

            # who has received a SECOND OR THIRD vaccination IN this period, and is in that age group? (dead or alive)

            df_fc_extra = df_p[ (df_p["year_secondvax"] == year) & ((df_p["week_nr_secondvax"] <= week_nr_thisyear) & (df_p["week_nr_secondvax"] > (week_nr_thisyear-weeksteps))) ]
            nr_vaxed_agegroup_thisweek_extra = len(df_fc_extra)
            nr_vax2_list.append(nr_vaxed_agegroup_thisweek_extra)
            df_fc_extra = df_p[ (df_p["year_thirdvax"] == year) & ((df_p["week_nr_thirdvax"] <= week_nr_thisyear) & (df_p["week_nr_thirdvax"] > (week_nr_thisyear-weeksteps))) ]
            nr_vaxed_agegroup_thisweek_extra = len(df_fc_extra)
            nr_vax3_list.append(nr_vaxed_agegroup_thisweek_extra)
            
            print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup_untilthen))
            print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup_untilthen))
            print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))
            perc_vaxed = 100.0 * float(nr_vaxed_agegroup_untilthen)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen ) # nr_p_ag
            print("perc_vaxed until then (among alive until then): " + str(perc_vaxed))

            perc_vaxed = 100.0 * float(nr_vaxed_agegroup_untilthen_incldead)/float(nr_p_ag) # nr_p_ag
            print("perc_vaxed until then (among whole starting population): " + str(perc_vaxed))
            perc_vaccinated_list.append(perc_vaxed)

        
            perc_diagnosis_novax = float(nr_diagnosis_novax)/float(nr_unvaxed_agegroup_untilthen) * 100.0
            if perc_diagnosis_novax > perc_diagnosis_maxval:
                perc_diagnosis_maxval = perc_diagnosis_novax
            if perc_diagnosis_novax < perc_diagnosis_minval:
                perc_diagnosis_minval = perc_diagnosis_novax

            perc_diagnosis_all = float(nr_diagnosis_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100.0
            if perc_diagnosis_all > perc_diagnosis_maxval:
                perc_diagnosis_maxval = perc_diagnosis_all
            if perc_diagnosis_all < perc_diagnosis_minval:
                perc_diagnosis_minval = perc_diagnosis_all
                       
            perc_diagnosis_all_list.append(perc_diagnosis_all)

            # perc_deaths_afterdiag_all = float(nr_deaths_afterdiag_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100.0
            # perc_deaths_afterdiag_vax = float(nr_deaths_afterdiag_vaxed)/float(nr_vaxed_agegroup_untilthen) * 100.0
            # perc_deaths_afterdiag_novax = float(nr_deaths_afterdiag_unvaxed)/float(nr_unvaxed_agegroup_untilthen) * 100.0
            perc_deaths_afterdiag_all = float(nr_deaths_afterdiag_all)/float(nr_diagnosis_all) * 100.0
            if nr_diagnosis_vax:
                perc_deaths_afterdiag_vax = float(nr_deaths_afterdiag_vaxed)/float(nr_diagnosis_vax) * 100.0
            else:
                perc_deaths_afterdiag_vax = 0
            perc_deaths_afterdiag_novax = float(nr_deaths_afterdiag_unvaxed)/float(nr_diagnosis_novax) * 100.0

            nr_deaths_afterdiag_all_list.append(nr_deaths_afterdiag_all)
            nr_deaths_afterdiag_vaxed_list.append(nr_deaths_afterdiag_vaxed)
            nr_deaths_afterdiag_unvaxed_list.append(nr_deaths_afterdiag_unvaxed)
            perc_deaths_afterdiag_all_list.append(perc_deaths_afterdiag_all)
            perc_deaths_afterdiag_vax_list.append(perc_deaths_afterdiag_vax)
            perc_deaths_afterdiag_novax_list.append(perc_deaths_afterdiag_novax)


            # perc_infected_beforediag_all = float(nr_infected_beforediag_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100.0
            # perc_infected_beforediag_vax = float(nr_infected_beforediag_vaxed)/float(nr_vaxed_agegroup_untilthen) * 100.0
            # perc_infected_beforediag_novax = float(nr_infected_beforediag_unvaxed)/float(nr_unvaxed_agegroup_untilthen) * 100.0
            perc_infected_beforediag_all = float(nr_infected_beforediag_all)/float(nr_diagnosis_all) * 100.0
            if nr_diagnosis_vax:
                perc_infected_beforediag_vax = float(nr_infected_beforediag_vaxed)/float(nr_diagnosis_vax) * 100.0
            else:
                perc_infected_beforediag_vax = 0
            perc_infected_beforediag_novax = float(nr_infected_beforediag_unvaxed)/float(nr_diagnosis_novax) * 100.0

            nr_infected_beforediag_all_list.append(nr_infected_beforediag_all)
            nr_infected_beforediag_vaxed_list.append(nr_infected_beforediag_vaxed)
            nr_infected_beforediag_unvaxed_list.append(nr_infected_beforediag_unvaxed)
            perc_infected_beforediag_all_list.append(perc_infected_beforediag_all)
            perc_infected_beforediag_vax_list.append(perc_infected_beforediag_vax)
            perc_infected_beforediag_novax_list.append(perc_infected_beforediag_novax)

            if perc_deaths_afterdiag_all > perc_deathinf_maxval:
                perc_deathinf_maxval = perc_deaths_afterdiag_all
            if perc_deaths_afterdiag_all < perc_deathinf_minval:
                perc_deathinf_minval = perc_deaths_afterdiag_all

            if perc_deaths_afterdiag_vax > perc_deathinf_maxval:
                perc_deathinf_maxval = perc_deaths_afterdiag_vax
            if perc_deaths_afterdiag_vax < perc_deathinf_minval:
                perc_deathinf_minval = perc_deaths_afterdiag_vax

            if perc_deaths_afterdiag_novax > perc_deathinf_maxval:
                perc_deathinf_maxval = perc_deaths_afterdiag_novax
            if perc_deaths_afterdiag_novax < perc_deathinf_minval:
                perc_deathinf_minval = perc_deaths_afterdiag_novax

            if perc_infected_beforediag_all > perc_deathinf_maxval:
                perc_deathinf_maxval = perc_infected_beforediag_all
            if perc_infected_beforediag_all < perc_deathinf_minval:
                perc_deathinf_minval = perc_infected_beforediag_all

            if perc_infected_beforediag_vax > perc_deathinf_maxval:
                perc_deathinf_maxval = perc_infected_beforediag_vax
            if perc_infected_beforediag_vax < perc_deathinf_minval:
                perc_deathinf_minval = perc_infected_beforediag_vax

            if perc_infected_beforediag_novax > perc_deathinf_maxval:
                perc_deathinf_maxval = perc_infected_beforediag_novax
            if perc_infected_beforediag_novax < perc_deathinf_minval:
                perc_deathinf_minval = perc_infected_beforediag_novax

            # nr_diagnosis_baseline = (perc_diagnosis_baseline/100.0) * float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) 
            # nr_diagnosis_baseline_list.append(nr_diagnosis_baseline)
            
            nr_diagnosis_vax_list.append(nr_diagnosis_vax)
            nr_diagnosis_novax_list.append(nr_diagnosis_novax)

            perc_diagnosis_vax_list.append(perc_diagnosis_vax)
            perc_diagnosis_novax_list.append(perc_diagnosis_novax)

            print()

            nr_unvaxed_agegroup_untilthen -= nr_deaths_novax
            nr_vaxed_agegroup_untilthen -= nr_deaths_vax

            nr_vaxed_alive_list.append(nr_vaxed_agegroup_untilthen)
            nr_unvaxed_alive_list.append(nr_unvaxed_agegroup_untilthen)

            # if nr_vaxed_agegroup_untilthen>1:
            #     if (nr_diagnosis_total + nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) != nr_p_ag:
            #         print("ERROR:")
            #         print("nr_diagnosis_total + nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) != nr_p_ag")
            #         exit(1)

            weeknr_list.append(weeknr)
            # if weeknr == 48:
            #     weeksteps = 4
            weeknr += weeksteps
            date_from = date_from + timedelta(weeks = weeksteps)
            date_to = date_from + timedelta(weeks = weeksteps)
            year_prev = year
            year = date_to.year
            nr_weeks_thisyear += 1

            # weeksteps = 8

        nr_diag_thisyear_avg = float(nr_diag_oneyear)/float(nr_periods)
        for j in range(nr_weeks_thisyear):
            nr_diag_thisyear_avg_list.append(nr_diag_thisyear_avg)

        print()
        print("Cleaning up for allowed output..")
        print()

        nr_vax1_list = [0 if v<10 else v for v in nr_vax1_list]
        nr_vax1_list = [int(round((float(v)/10.0),0)*10) if (v>10) else v for v in nr_vax1_list]
        nr_vax2_list = [0 if v<10 else v for v in nr_vax2_list]
        nr_vax2_list = [int(round((float(v)/10.0),0)*10) if (v>10) else v for v in nr_vax2_list]
        nr_vax3_list = [0 if v<10 else v for v in nr_vax3_list]
        nr_vax3_list = [int(round((float(v)/10.0),0)*10) if (v>10) else v for v in nr_vax3_list]

        nr_vaxed_alive_list = [0 if v<10 else v for v in nr_vaxed_alive_list]
        nr_vaxed_alive_list = [int(round((float(v)/10.0),0)*10) if (v>10) else v for v in nr_vaxed_alive_list]
        # nr_vaxed_alive_list = [0 if v<10 else v for v in nr_vaxed_alive_list]
        # nr_unvaxed_alive_list = [0 if v<10 else v for v in nr_unvaxed_alive_list]
        nr_unvaxed_alive_list = [0 if v<10 else v for v in nr_unvaxed_alive_list]
        nr_unvaxed_alive_list = [int(round((float(v)/10.0),0)*10) if (v>10) else v for v in nr_unvaxed_alive_list]

        nr_diagnosis_list = [0 if v<10 else v for v in nr_diagnosis_list]
        nr_diagnosis_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_diagnosis_list]
        nr_diagnosis_vax_list = [0 if v<10 else v for v in nr_diagnosis_vax_list]
        nr_diagnosis_vax_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_diagnosis_vax_list]
        nr_diagnosis_novax_list = [0 if v<10 else v for v in nr_diagnosis_novax_list]
        nr_diagnosis_novax_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_diagnosis_novax_list]

        for idx, val in enumerate(nr_vaxed_alive_list):
            if val<10:
                nr_vaxed_alive_list[idx]=0
                # nr_deaths_vax_list[idx]=0
                perc_diagnosis_vax_list[idx]=0
                perc_deaths_afterdiag_vax_list[idx]=0
                perc_infected_beforediag_vax_list[idx]=0
                nr_diagnosis_vax_list[idx]=0

        for idx, val in enumerate(nr_unvaxed_alive_list):
            if val<10:
                nr_unvaxed_alive_list[idx]=0
                # nr_deaths_vax_list[idx]=0
                perc_diagnosis_novax_list[idx]=0
                perc_deaths_afterdiag_novax_list[idx]=0
                perc_infected_beforediag_novax_list[idx]=0
                nr_diagnosis_novax_list[idx]=0

        for idx, val in enumerate(nr_diagnosis_vax_list):
            if val<10:
                nr_diagnosis_vax_list[idx]=0
                # nr_deaths_vax_list[idx]=0
                perc_diagnosis_vax_list[idx]=0
                perc_deaths_afterdiag_vax_list[idx]=0
                perc_infected_beforediag_vax_list[idx]=0
                perc_diagnosis_all_list[idx]=perc_diagnosis_novax_list[idx]
                perc_deaths_afterdiag_all_list[idx]=perc_deaths_afterdiag_novax_list[idx]
                perc_infected_beforediag_all_list[idx]=perc_infected_beforediag_novax_list[idx]

        for idx, val in enumerate(nr_diagnosis_novax_list):
            if val<10:
                nr_diagnosis_novax_list[idx]=0
                # nr_deaths_vax_list[idx]=0
                perc_diagnosis_novax_list[idx]=0
                perc_deaths_afterdiag_novax_list[idx]=0
                perc_infected_beforediag_novax_list[idx]=0
                perc_diagnosis_all_list[idx]=perc_diagnosis_vax_list[idx]
                perc_deaths_afterdiag_all_list[idx]=perc_deaths_afterdiag_vax_list[idx]
                perc_infected_beforediag_all_list[idx]=perc_infected_beforediag_vax_list[idx]


        fig,axs = plt.subplots(3,4) # , sharex=True

        # VACCINATIONS, POPULATION
        axs[0,0].plot(weeknr_list,nr_vax1_list, color = 'b', linestyle='solid', label='#1') #, label='vax 1 administered' , lw=2
        axs[0,0].plot(weeknr_list,nr_vax2_list, color = 'm', linestyle='solid', label='#2')
        axs[0,0].plot(weeknr_list,nr_vax3_list, color = 'y', linestyle='solid', label='#3')
        axs[0,0].legend()
        # axs[0,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[0,1].ylabel('number')
        axs[0,0].set(ylabel='number')
        # axs[0,0].set(xlabel='week number')
        axs[0,0].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[0,0].set_title('Vaccinations') #  (#1)
        axs[0,0].grid()

        # perc_vaccinated_list, nr_diagnosis_list
        axs[0,1].plot(weeknr_list,perc_vaccinated_list, color = 'b', linestyle='solid') #, label='vax 1 administered' , lw=2
        # axs[0,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[0,1].ylabel('number')
        axs[0,1].set(ylabel='%')
        # axs[0,0].set(xlabel='week number')
        axs[0,1].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[0,1].set_title('Vaccination rate')
        axs[0,1].set_ylim([-2,105])
        axs[0,1].grid()

        axs[0,2].plot(weeknr_list,nr_vaxed_alive_list, color = 'g', linestyle='solid', label='Vaccinated, alive') #, label='vax 1 administered' , lw=2
        axs[0,2].plot(weeknr_list,nr_unvaxed_alive_list, color = 'r', linestyle='solid', label='Unvaccinated, alive')
        axs[0,2].legend()
        axs[0,2].set(ylabel='number')
        axs[0,2].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[0,2].set_title('Vaccinated/unvaccinated population, alive')
        axs[0,2].grid()

        # nr_infected_beforediag_all_list = []
        # nr_infected_beforediag_vaxed_list = []
        # nr_infected_beforediag_unvaxed_list = []
        # perc_infected_beforediag_all_list = []
        # perc_infected_beforediag_vax_list = []
        # perc_infected_beforediag_novax_list = []

        axs[0,3].plot(weeknr_list,nr_diagnosis_vax_list, color = 'g', linestyle='solid', label='Vaccinated, diagnosis')
        axs[0,3].plot(weeknr_list,nr_diagnosis_novax_list, color = 'r', linestyle='solid', label='Unvaccinated, diagnosis')
        axs[0,3].legend()
        axs[0,3].set(ylabel='number')
        axs[0,3].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[0,3].set_title('Number of diagnoses, vaccinated/unvaccinated')
        axs[0,3].grid()
        

        # axs[1,0].plot(weeknr_list,nr_diagnosis_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,0].plot(weeknr_list,nr_diagnosis_list, color = 'b', linestyle='solid', label='diagnosis') #, label='vax 1 administered' , lw=2
        # axs[1,0].plot(weeknr_list,nr_diagnosis_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,0].legend()
        # axs[0,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[0,1].ylabel('number')
        axs[1,0].set(ylabel='number')
        # axs[0,0].set(xlabel='week number')
        axs[1,0].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[1,0].set_title('Diagnosis counts')
        axs[1,0].grid()

        # axs[1,1].plot(weeknr_list,perc_diagnosis_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,1].plot(weeknr_list,perc_diagnosis_all_list, color = 'b', linestyle='solid', label='diagnosis') # , marker='o' ; dotted, label='diagnosis all (per 100,000)' , lw=2
        # axs[1,1].plot(weeknr_list,perc_diagnosis_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,1].legend()
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[1,1].set(ylabel='%')
        # axs[1,0].set(xlabel='week number')
        axs[1,1].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[1,1].set_title('Diagnoses all (%)')
        axs[1,1].set_ylim([perc_diagnosis_minval,perc_diagnosis_maxval])
        axs[1,1].grid()

        # axs[1,2].plot(weeknr_list,perc_diagnosis_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,2].plot(weeknr_list,perc_diagnosis_vax_list, color = 'g', linestyle='solid', label='diagnosis') # , label='diagnosis vaccinated (per 100,000)'
        # axs[1,2].plot(weeknr_list,perc_diagnosis_vax_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,2].legend()
        # axs[1,0].xticks(range(0, 52*nr_years + 2, 52))
        # axs[1,0].ylabel('diagnosis per 100,000')
        axs[1,2].set(ylabel='%')
        # axs[1,1].set(xlabel='week number')
        axs[1,2].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[1,2].set_title('Diagnoses vaccinated (%)')
        axs[1,2].set_ylim([perc_diagnosis_minval,perc_diagnosis_maxval])
        axs[1,2].grid()

        # axs[1,3].plot(weeknr_list,perc_diagnosis_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,3].plot(weeknr_list,perc_diagnosis_novax_list, color = 'r', linestyle='solid', label='diagnosis') # dashed, label='diagnosis unvaccinated (per 100,000)'
        # axs[1,3].plot(weeknr_list,perc_diagnosis_novax_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,3].legend()
        # axs[1,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[1,1].ylabel('diagnosis per 100,000')
        axs[1,3].set(ylabel='%')
        # axs[1,2].set(xlabel='week number')
        axs[1,3].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[1,3].set_title('Diagnoses unvaccinated (%)')  
        axs[1,3].set_ylim([perc_diagnosis_minval,perc_diagnosis_maxval]) 
        axs[1,3].grid()

        # nr_diag_thisyear_avg_list
        axs[2,0].plot(weeknr_list,nr_diag_thisyear_avg_list, color = 'b', linestyle='solid') # , label='diagnosis mean per period'
        # axs[2,0].plot(weeknr_list,nr_deaths_afterdiag_all_list, color = 'k', linestyle='solid', label='death after diagnosis')
        # axs[2,0].plot(weeknr_list,nr_infected_beforediag_all_list, color = 'orange', linestyle='solid', label='infected before diagnosis')
        # axs[2,0].legend()
        axs[2,0].set(ylabel='number')
        axs[2,0].set_xticks(range(0, 52*nr_years + 2, 26))
        # axs[2,0].set_title('Events before/after')
        axs[2,0].set_title('Diagnosis mean per period')
        axs[2,0].grid()

        axs[2,1].plot(weeknr_list,perc_deaths_afterdiag_all_list, color = 'k', linestyle='solid', label='event after') # 'death after diagnosis'
        axs[2,1].plot(weeknr_list,perc_infected_beforediag_all_list, color = 'orange', linestyle='solid', label='event before') # 'infected before diagnosis'
        axs[2,1].legend()
        axs[2,1].set(ylabel='%')
        axs[2,1].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[2,1].set_title('Events before/after (%)')
        axs[2,1].set_ylim([perc_deathinf_minval,perc_deathinf_maxval])
        axs[2,1].grid()

        axs[2,2].plot(weeknr_list,perc_deaths_afterdiag_vax_list, color = 'k', linestyle='solid', label='event after')
        axs[2,2].plot(weeknr_list,perc_infected_beforediag_vax_list, color = 'orange', linestyle='solid', label='event before')
        axs[2,2].legend()
        axs[2,2].set(ylabel='%')
        axs[2,2].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[2,2].set_title('Events before/after, vaccinated (%)')
        axs[2,2].set_ylim([perc_deathinf_minval,perc_deathinf_maxval])
        axs[2,2].grid()

        axs[2,3].plot(weeknr_list,perc_deaths_afterdiag_novax_list, color = 'k', linestyle='solid', label='event after')
        axs[2,3].plot(weeknr_list,perc_infected_beforediag_novax_list, color = 'orange', linestyle='solid', label='event before')
        axs[2,3].legend()
        axs[2,3].set(ylabel='%')
        axs[2,3].set_xticks(range(0, 52*nr_years + 2, 26))
        axs[2,3].set_title('Events before/after, unvaccinated (%)')
        axs[2,3].set_ylim([perc_deathinf_minval,perc_deathinf_maxval])
        axs[2,3].grid()

        precision = 4
        precisionlow = 1

        perc_vaccinated_list = [f"{number:.{precisionlow}f}" for number in perc_vaccinated_list]
        nr_diag_thisyear_avg_list = [f"{number:.{precisionlow}f}" for number in nr_diag_thisyear_avg_list]

        perc_diagnosis_vax_list = [f"{number:.{precision}f}" for number in perc_diagnosis_vax_list]
        perc_diagnosis_novax_list = [f"{number:.{precision}f}" for number in perc_diagnosis_novax_list]
        perc_diagnosis_all_list = [f"{number:.{precision}f}" for number in perc_diagnosis_all_list]

        perc_deaths_afterdiag_vax_list = [f"{number:.{precision}f}" for number in perc_deaths_afterdiag_vax_list]
        perc_deaths_afterdiag_novax_list = [f"{number:.{precision}f}" for number in perc_deaths_afterdiag_novax_list]
        perc_deaths_afterdiag_all_list = [f"{number:.{precision}f}" for number in perc_deaths_afterdiag_all_list]
        perc_infected_beforediag_vax_list = [f"{number:.{precision}f}" for number in perc_infected_beforediag_vax_list]
        perc_infected_beforediag_novax_list = [f"{number:.{precision}f}" for number in perc_infected_beforediag_novax_list]
        perc_infected_beforediag_all_list = [f"{number:.{precision}f}" for number in perc_infected_beforediag_all_list]

       
        df_out = pd.DataFrame()
        df_out["weeknr_list"] = weeknr_list
        df_out["nr_vax1_list"] = nr_vax1_list
        df_out["nr_vax2_list"] = nr_vax2_list
        df_out["nr_vax3_list"] = nr_vax3_list
        df_out["perc_vaccinated_list"] = perc_vaccinated_list
        df_out["nr_vaxed_alive_list"] = nr_vaxed_alive_list
        df_out["nr_unvaxed_alive_list"] = nr_unvaxed_alive_list

        # df_out["nr_diagnosis_vax_list"] = nr_diagnosis_vax_list
        # df_out["nr_diagnosis_novax_list"] = nr_diagnosis_novax_list
        df_out["nr_diagnosis_list"] = nr_diagnosis_list
        df_out["perc_diagnosis_all_list"] = perc_diagnosis_all_list
        df_out["perc_diagnosis_vax_list"] = perc_diagnosis_vax_list
        df_out["perc_diagnosis_novax_list"] = perc_diagnosis_novax_list
        
        df_out["nr_diag_thisyear_avg_list"] = nr_diag_thisyear_avg_list
        df_out["perc_events_after_all_list"] = perc_deaths_afterdiag_all_list
        df_out["perc_events_before_all_list"] = perc_infected_beforediag_all_list
        df_out["perc_events_after_vax_list"] = perc_deaths_afterdiag_vax_list
        df_out["perc_events_before_vax_list"] = perc_infected_beforediag_vax_list
        df_out["perc_events_after_novax_list"] = perc_deaths_afterdiag_novax_list
        df_out["perc_events_before_novax_list"] = perc_infected_beforediag_novax_list


        filename_csv = "H:/data/output/csv_python/ves/" + mat_str + "/diagn_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels)+ "_W" + str(weeksteps)+ versionstr 
        if booster:
            filename_csv += "_BOOSTER"
        print("writing: "+filename_csv+ ".csv")
        df_out.to_csv(filename_csv+ ".csv")

        # plt.tight_layout()
        plt.subplots_adjust(hspace = 0.5)

        suptitle_str = "Age group " + str(birthyear_from) +"-" + str(birthyear_to) +", " + mat_str + " " + versionstr +", WLZ " + str(wlz_bit) +", RxRisk LevelsType " + str(med_rxrisk_scores) + ", WLZ LevelsType " + str(wlz_levels) + ", W" + str(weeksteps) +", "+ yearsstr
        if booster:
            suptitle_str += ", BOOSTER"
        plt.suptitle(suptitle_str)
        manager = plt.get_current_fig_manager()
        # manager.window.state('zoomed')
        # # manager.window.showMaximized()
        manager.full_screen_toggle()
        
        # versionstr = "_v0"
        figfilestr = "H:/data/output/plots/ves/" + mat_str + "/diagn_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + "_W" + str(weeksteps) + versionstr
        if booster:
            figfilestr += "_BOOSTER"
        plt.savefig(figfilestr + ".pdf", format="pdf", bbox_inches="tight")
        # plt.savefig("H:/data/plots/hist_diagnosis_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
        manager.full_screen_toggle()
        plt.show() # block=False

    return


