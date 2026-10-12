import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import date, datetime, timedelta
import time

def add_extra_analysis_data(df_p):
    df_p = df_p.copy()
    print("adding some extra analysis data..")
    df_p["week_nr_dead"] = -1
    df_p["year_dead"] = -1

    m = ( (df_p["dead_bit"]==1) )
    df_p.loc[m, "week_nr_dead"] = df_p.loc[m, "dead_date"].dt.isocalendar().week
    df_p.loc[m, "year_dead"] = df_p.loc[m, "dead_date"].dt.isocalendar().year

    df_p["covid_vax_seconddate"] = None
    df_p["covid_vax_thirddate"] = None
    df_p["week_nr_secondvax"] = -1
    df_p["year_secondvax"] = -1
    df_p["week_nr_thirdvax"] = -1
    df_p["year_thirdvax"] = -1

    start = time.time()
    for index, rowdata in df_p.iterrows():
        if index % 100000 == 0:
            print(index)
            # print(rowdata)      
            print(time.time() - start)
            start = time.time()
            print()
        
        # DOOD
        covid_vax_dates_str = rowdata["covid_vax_dates"]
        if covid_vax_dates_str is not None and len(covid_vax_dates_str):
            nr_covid_vax = int(rowdata["nr_covid_vax"])
            if nr_covid_vax>1:
                date_list = covid_vax_dates_str.split(";")
                df_p.at[index, "covid_vax_seconddate"] = date_list[1]
            if nr_covid_vax>2:
                df_p.at[index, "covid_vax_thirddate"] = date_list[2]

    # df_p["vaccinated_2"] = 0
    # m = ( (df_p['nr_covid_vax'].notnull()==True) & (df_p['nr_covid_vax']>1) )
    # df_p.loc[m, "vaccinated_2"] = 1
    df_p["covid_vax_seconddate"] = pd.to_datetime(df_p["covid_vax_seconddate"])
    df_p["covid_vax_thirddate"] = pd.to_datetime(df_p["covid_vax_thirddate"])

    m = ( (df_p['covid_vax_seconddate'].notnull()==True) )
    df_p.loc[m, "week_nr_secondvax"] = df_p.loc[m, "covid_vax_seconddate"].dt.isocalendar().week     
    df_p.loc[m, "year_secondvax"] = df_p.loc[m, "covid_vax_seconddate"].dt.isocalendar().year

    m = ( (df_p['covid_vax_thirddate'].notnull()==True) )
    df_p.loc[m, "week_nr_thirdvax"] = df_p.loc[m, "covid_vax_thirddate"].dt.isocalendar().week     
    df_p.loc[m, "year_thirdvax"] = df_p.loc[m, "covid_vax_thirddate"].dt.isocalendar().year

    return df_p


def calc_deaths_per_period(df_p, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, weeksteps, mat_str, versionstr, booster=False):
    basepath = "H:/data/"
    year = 2021 # 2019 # 2018 2021 # 
    refyear = year
    year_tostop = 2024 #2022 #  
    nr_years = year_tostop - year

    min_nr_vaxed = 100
    # 
    yearsstr = "2021-2023" # "2021" #"2019-2022" # 
    year_prev = year - 1
    
    print("First year:")
    print(year)

    age_from = refyear - birthyear_to
    age_to = refyear - birthyear_from
    birthyear_diff = birthyear_to - birthyear_from
    if birthyear_diff==10:
        filename_core = "deaths_baseline_" + str(age_from) + "_" + str(age_to) + "_v0"
    elif birthyear_diff==20:
        filename_core = "deaths_baseline_" + str(age_from) + "_" + str(age_to) + "_" + str(weeksteps) + "_v0"
    filename_ftr = basepath+"python_pandas/deaths_baselines/"+filename_core+".ftr"
    df_db = pd.read_feather(filename_ftr) # baseline deaths for this age group!

    # age_from = 70 # 50 # 15 # 65 # 10 # 15 # 60 50 40 # 
    # age_to = 125 # 65 # 50 # 125 # 50 # 45 # 90 75 65 # 

    # df_p = df_p[ (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) & 
    #              (df_p['WLZ_bit']==wlz_bit) ] # &  ((df_p['jaar_overlijden']>=year) | (df_p['jaar_overlijden']==-1))
    
    if wlz_bit==0:
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
    df_p_test = df_p[ (df_p['year_dead']==year)  ]
    print("Number of people in this age group who died this year : " + str(len(df_p_test))) 

    if nr_p_ag==0:
        print("Number of people alive and present in this age group is zero! Ending this analysis for this group")
    else:
    # print(df_p.head(10))
    # versionstr = "_v1"

        date_from = date(year,1,1)
        date_to = date_from + timedelta(weeks = weeksteps)

        weeknr = 0 + weeksteps
        nr_deaths_list = []
        nr_deaths_vax_list = []
        nr_deaths_novax_list = []
        perc_deaths_vax_list = []
        perc_deaths_novax_list = []
        perc_deaths_all_list = []
        nr_vax1_list = []

        perc_deaths_vax_covid_list = []
        perc_deaths_vax_noncovid_list = []
        perc_deaths_novax_covid_list = []
        perc_deaths_novax_noncovid_list = []

        VE_RRR_ACM_list = []
        VE_ARR_ACM_list = []
        VE_RRR_covid_list = []
        VE_ARR_covid_list = []
        VE_RRR_noncovid_list = []
        VE_ARR_noncovid_list = []

        perc_vaccinated_list = []

        perc_deaths_covid_list = []
        # perc_deaths_noncovid_list = []
        nr_deaths_covid_list = []
        # nr_deaths_noncovid_list = []

        # nr_deaths_vax_list = []
        # nr_deaths_novax_list = []
        nr_vaxed_alive_list = []
        nr_unvaxed_alive_list = []

        nr_vax2_list = []
        nr_vax3_list = []
        # nr_vax4_list = []
        # nr_vax5_list = []
        weeknr_list = []

        perc_U_vax_list = []
        perc_I_vax_list = []
        perc_C_vax_list = []
        perc_X_vax_list = []
        perc_U_unvax_list = []
        perc_I_unvax_list = []
        perc_C_unvax_list = []
        perc_X_unvax_list = []

        perc_deaths_baseline_list = []
        nr_deaths_baseline_list = []

        nr_vaxed_agegroup_untilthen = 0
        nr_vaxed_agegroup_untilthen_incldead = 0
        nr_unvaxed_agegroup_untilthen = nr_p_ag - nr_vaxed_agegroup_untilthen

        perc_deaths_maxval = -1.0
        VE_RRR_minval=99999.0
        VE_RRR_maxval=-99999.0
        VE_ARR_minval=99999.0
        VE_ARR_maxval=-99999.0
        nr_deaths_total = 0
        while year<year_tostop: # and weeknr <=6:
            if year > year_prev:
                # yearstr = str(year)
                print(year)
                i_year_predict = year-refyear
                print(i_year_predict)

                df_p_test = df_p[ (df_p['year_dead']==year)  ]
                print("Number of people in this age group who died this year : " + str(len(df_p_test))) 

                # nr_p_ag += nr_deaths_all_year
                # print("Number of people in this age group in this year: " + str(nr_p_ag))

                # who has received a vaccination before the start of this period, and is in that age group?
                # df_fc = df_cims[ (df_cims["datetimeobj_prik"] < (date_from)) &  #  - timedelta(weeks = 2)                                
                #                     (df_cims["prik_nummer"] == 1) ]           
                # nr_vaxed_agegroup_untilthen = df_fc['RINPERSOON'].nunique()

                print("nr_vaxed_agegroup_untilthen: " + str(nr_vaxed_agegroup_untilthen))
                print("nr_unvaxed_agegroup_untilthen: " + str(nr_unvaxed_agegroup_untilthen))
                print("sum: " + str(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen))

            print(weeknr)
            print(date_from)
            print(date_to)
            week_nr_thisyear = date_to.isocalendar().week
            print(week_nr_thisyear)
            # print("selecting deaths in " + yearstr)

            # Who died in this period?
            df_pd = df_p[ (df_p["year_dead"] == year) & ((df_p["week_nr_dead"] <= week_nr_thisyear) & (df_p["week_nr_dead"] > (week_nr_thisyear-weeksteps))) ]
            nr_deaths_all = len(df_pd)
            nr_deaths_list.append(nr_deaths_all)
            nr_deaths_total += nr_deaths_all

            rows = df_db.loc[ (df_db["week_nr_thisyear"] == week_nr_thisyear) ]
            if len(rows):
                perc_deaths_baseline = rows.iloc[0][str(i_year_predict)]
            else:
                perc_deaths_baseline = math.nan
            perc_deaths_baseline_list.append(perc_deaths_baseline)

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

            # select those deaths in this period that are also vaccinated
            df_ovax = df_pd[df_pd["treatment"]==1]
            # df['Rinpersoon'].nunique()
            nr_deaths_vax = len(df_ovax)
            # nr_deaths_vax = df_ovax['RINPERSOON'].nunique()
            perc_deaths_vax = float(nr_deaths_vax)/float(nr_vaxed_agegroup_untilthen) * 100.0
            if perc_deaths_vax > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_vax

            nr_deaths_novax = nr_deaths_all - nr_deaths_vax

            print("nr_deaths_all: " + str(nr_deaths_all))
            print("nr_deaths_vax: " + str(nr_deaths_vax))
            print("nr_deaths_novax (calc INDIRECTLY from all and vaxed dead data): " + str(nr_deaths_novax))
            
            df_onovax = df_pd[df_pd["control"]==1]
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
            
            # CAUSES OF DEATH, VAXED:
            df_vax_covid = df_ovax[df_ovax["dead_bit_covid"]==1]
            df_vax_noncovid = df_ovax[df_ovax["dead_bit_noncovid"]==1]
            nr_dead_vax_covid = len(df_vax_covid)
            nr_dead_vax_noncovid = len(df_vax_noncovid)
            print("Vaccinated: nr_dead_vax_covid: " + str(nr_dead_vax_covid))
            print("Vaccinated: nr_dead_vax_noncovid: " + str(nr_dead_vax_noncovid))

            # CAUSES OF DEATH, VAXED, MORE DETAIL:
            nr_U_ICD10 = len( df_ovax[df_ovax['dead_cause'].str.startswith('U')] ) # Covid
            nr_I_ICD10 = len( df_ovax[ (df_ovax['dead_cause'].str.startswith('I')) | 
                                      (df_ovax['dead_cause'].str.startswith('R9'))] ) # Cardiovascular and 'Sudden/Unknown'
            nr_C_ICD10 = len( df_ovax[ (df_ovax['dead_cause'].str.startswith('C')) | 
                                    (df_ovax['dead_cause'].str.startswith('D0')) |
                                    (df_ovax['dead_cause'].str.startswith('D1')) |
                                    (df_ovax['dead_cause'].str.startswith('D2')) |
                                    (df_ovax['dead_cause'].str.startswith('D3')) |
                                    (df_ovax['dead_cause'].str.startswith('D4')) ] ) # Cancer
            nr_X_ICD10 = nr_deaths_vax - (nr_U_ICD10+nr_I_ICD10+nr_C_ICD10)
            # len( df_ovax[ (df_ovax['dead_cause'].str.startswith('X')) | 
            #                         (df_ovax['dead_cause'].str.startswith('Y')) ] ) # External
            
            if nr_deaths_vax>0:
                perc_U = float(nr_U_ICD10)/float(nr_deaths_vax) * 100.0
                perc_I = float(nr_I_ICD10)/float(nr_deaths_vax) * 100.0
                perc_C = float(nr_C_ICD10)/float(nr_deaths_vax) * 100.0
                perc_X = float(nr_X_ICD10)/float(nr_deaths_vax) * 100.0
            else:
                perc_U = math.nan
                perc_I = math.nan 
                perc_C = math.nan
                perc_X = math.nan
            perc_U_vax_list.append(perc_U)
            perc_I_vax_list.append(perc_I)
            perc_C_vax_list.append(perc_C)
            perc_X_vax_list.append(perc_X)

            # CAUSES OF DEATH, UNVAXED:
            df_novax_covid = df_onovax[df_onovax["dead_bit_covid"]==1]
            df_novax_noncovid = df_onovax[df_onovax["dead_bit_noncovid"]==1]
            nr_dead_novax_covid = len(df_novax_covid)
            nr_dead_novax_noncovid = len(df_novax_noncovid)
            print("Unvaccinated: nr_dead_novax_covid: " + str(nr_dead_novax_covid))
            print("Unvaccinated: nr_dead_novax_noncovid: " + str(nr_dead_novax_noncovid))

             # CAUSES OF DEATH, UNVAXED, MORE DETAIL:
            nr_U_ICD10 = len( df_onovax[df_onovax['dead_cause'].str.startswith('U')] ) # Covid
            nr_I_ICD10 = len( df_onovax[ (df_onovax['dead_cause'].str.startswith('I')) | 
                                      (df_onovax['dead_cause'].str.startswith('R9'))] ) # Cardiovascular and 'Sudden/Unknown'
            nr_C_ICD10 = len( df_onovax[ (df_onovax['dead_cause'].str.startswith('C')) | 
                                    (df_onovax['dead_cause'].str.startswith('D0')) |
                                    (df_onovax['dead_cause'].str.startswith('D1')) |
                                    (df_onovax['dead_cause'].str.startswith('D2')) |
                                    (df_onovax['dead_cause'].str.startswith('D3')) |
                                    (df_onovax['dead_cause'].str.startswith('D4')) ] ) # Cancer
            nr_X_ICD10 = nr_deaths_novax - (nr_U_ICD10+nr_I_ICD10+nr_C_ICD10)
            # len( df_onovax[ (df_onovax['dead_cause'].str.startswith('X')) | 
            #                         (df_onovax['dead_cause'].str.startswith('Y')) ] ) # External
            
            if nr_deaths_novax>0:
                perc_U = float(nr_U_ICD10)/float(nr_deaths_novax) * 100.0
                perc_I = float(nr_I_ICD10)/float(nr_deaths_novax) * 100.0
                perc_C = float(nr_C_ICD10)/float(nr_deaths_novax) * 100.0
                perc_X = float(nr_X_ICD10)/float(nr_deaths_novax) * 100.0
            else:
                perc_U = math.nan
                perc_I = math.nan 
                perc_C = math.nan
                perc_X = math.nan
            perc_U_unvax_list.append(perc_U)
            perc_I_unvax_list.append(perc_I)
            perc_C_unvax_list.append(perc_C)
            perc_X_unvax_list.append(perc_X)
        
            perc_deaths_novax = float(nr_deaths_novax)/float(nr_unvaxed_agegroup_untilthen) * 100.0
            if perc_deaths_novax > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_novax

            perc_deaths_all = float(nr_deaths_all)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100.0
            if perc_deaths_all > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_all
                       
            perc_deaths_all_list.append(perc_deaths_all)

            nr_deaths_baseline = (perc_deaths_baseline/100.0) * float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) 
            nr_deaths_baseline_list.append(nr_deaths_baseline)
            
            nr_deaths_vax_list.append(nr_deaths_vax)
            nr_deaths_novax_list.append(nr_deaths_novax)

            # ** ALL CAUSE MORTALITY **
            perc_deaths_vax_list.append(perc_deaths_vax)
            perc_deaths_novax_list.append(perc_deaths_novax)

            perc_deaths_vax_covid = float(nr_dead_vax_covid)/float(nr_vaxed_agegroup_untilthen) * 100.0
            if perc_deaths_vax_covid > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_vax_covid
            perc_deaths_vax_noncovid = float(nr_dead_vax_noncovid)/float(nr_vaxed_agegroup_untilthen) * 100.0
            if perc_deaths_vax_noncovid > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_vax_noncovid

            perc_deaths_novax_covid = float(nr_dead_novax_covid)/float(nr_unvaxed_agegroup_untilthen) * 100.0
            if perc_deaths_novax_covid > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_novax_covid
            perc_deaths_novax_noncovid = float(nr_dead_novax_noncovid)/float(nr_unvaxed_agegroup_untilthen) * 100.0
            if perc_deaths_novax_noncovid > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_novax_noncovid

            nr_deaths_covid = nr_dead_vax_covid+nr_dead_novax_covid
            perc_deaths_covid = float(nr_deaths_covid)/float(nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) * 100.0
            if perc_deaths_covid > perc_deaths_maxval:
                perc_deaths_maxval = perc_deaths_covid

            nr_deaths_covid_list.append(nr_deaths_covid)

            perc_deaths_vax_covid_list.append(perc_deaths_vax_covid)
            perc_deaths_vax_noncovid_list.append(perc_deaths_vax_noncovid)
            perc_deaths_novax_covid_list.append(perc_deaths_novax_covid)
            perc_deaths_novax_noncovid_list.append(perc_deaths_novax_noncovid)

            perc_deaths_covid_list.append(perc_deaths_covid)

            if perc_deaths_novax==0 or nr_vaxed_agegroup_untilthen<min_nr_vaxed:
                VE_RRR_ACM = 0
            else:
                VE_RRR_ACM = (perc_deaths_novax-perc_deaths_vax)/perc_deaths_novax * 100.0
            print("VE_RRR_ACM: " + str(VE_RRR_ACM))
            if nr_vaxed_agegroup_untilthen<min_nr_vaxed:
                VE_ARR_ACM = 0
            else:
                VE_ARR_ACM = (perc_deaths_novax-perc_deaths_vax) # / 1000.0
            print("VE_ARR_ACM: " + str(VE_ARR_ACM))
            if VE_RRR_ACM<VE_RRR_minval:
                VE_RRR_minval=VE_RRR_ACM
            if VE_RRR_ACM>VE_RRR_maxval:
                VE_RRR_maxval=VE_RRR_ACM
            if VE_ARR_ACM<VE_ARR_minval:
                VE_ARR_minval=VE_ARR_ACM
            if VE_ARR_ACM>VE_ARR_maxval:
                VE_ARR_maxval=VE_ARR_ACM

            if perc_deaths_novax_covid==0 or nr_vaxed_agegroup_untilthen<min_nr_vaxed:
                VE_RRR_covid = 0
            else:
                VE_RRR_covid = (perc_deaths_novax_covid-perc_deaths_vax_covid)/perc_deaths_novax_covid * 100.0
            print("VE_RRR_covid: " + str(VE_RRR_covid))
            if nr_vaxed_agegroup_untilthen<min_nr_vaxed:
                VE_ARR_covid = 0
            else:
                VE_ARR_covid = (perc_deaths_novax_covid-perc_deaths_vax_covid) # / 1000.0
            print("VE_ARR_covid: " + str(VE_ARR_covid))
            if VE_RRR_covid<VE_RRR_minval:
                VE_RRR_minval=VE_RRR_covid
            if VE_RRR_covid>VE_RRR_maxval:
                VE_RRR_maxval=VE_RRR_covid
            if VE_ARR_covid<VE_ARR_minval:
                VE_ARR_minval=VE_ARR_covid
            if VE_ARR_covid>VE_ARR_maxval:
                VE_ARR_maxval=VE_ARR_covid

            if perc_deaths_novax_noncovid==0 or nr_vaxed_agegroup_untilthen<min_nr_vaxed:
                VE_RRR_noncovid = 0
            else:
                VE_RRR_noncovid = (perc_deaths_novax_noncovid-perc_deaths_vax_noncovid)/perc_deaths_novax_noncovid * 100.0
            print("VE_RRR_noncovid: " + str(VE_RRR_noncovid))
            if nr_vaxed_agegroup_untilthen<min_nr_vaxed:
                VE_ARR_noncovid = 0
            else:
                VE_ARR_noncovid = (perc_deaths_novax_noncovid-perc_deaths_vax_noncovid) # / 1000.0
            print("VE_ARR_noncovid: " + str(VE_ARR_noncovid))
            if VE_RRR_noncovid<VE_RRR_minval:
                VE_RRR_minval=VE_RRR_noncovid
            if VE_RRR_noncovid>VE_RRR_maxval:
                VE_RRR_maxval=VE_RRR_noncovid
            if VE_ARR_noncovid<VE_ARR_minval:
                VE_ARR_minval=VE_ARR_noncovid
            if VE_ARR_noncovid>VE_ARR_maxval:
                VE_ARR_maxval=VE_ARR_noncovid

            VE_RRR_ACM_list.append(VE_RRR_ACM)
            VE_ARR_ACM_list.append(VE_ARR_ACM)
            VE_RRR_covid_list.append(VE_RRR_covid)
            VE_ARR_covid_list.append(VE_ARR_covid)
            VE_RRR_noncovid_list.append(VE_RRR_noncovid)
            VE_ARR_noncovid_list.append(VE_ARR_noncovid)

            print()

            nr_unvaxed_agegroup_untilthen -= nr_deaths_novax
            nr_vaxed_agegroup_untilthen -= nr_deaths_vax

            nr_vaxed_alive_list.append(nr_vaxed_agegroup_untilthen)
            nr_unvaxed_alive_list.append(nr_unvaxed_agegroup_untilthen)

            # if nr_vaxed_agegroup_untilthen>1:
            #     if (nr_deaths_total + nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) != nr_p_ag:
            #         print("ERROR:")
            #         print("nr_deaths_total + nr_unvaxed_agegroup_untilthen + nr_vaxed_agegroup_untilthen) != nr_p_ag")
            #         exit(1)

            weeknr_list.append(weeknr)
            weeknr += weeksteps
            date_from = date_from + timedelta(weeks = weeksteps)
            date_to = date_from + timedelta(weeks = weeksteps)
            year_prev = year
            year = date_to.year


        print()
        print("Cleaning up for allowed output..")
        print()

        nr_vax1_list = [0 if v<10 else v for v in nr_vax1_list]
        nr_vax1_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_vax1_list]
        nr_vax2_list = [0 if v<10 else v for v in nr_vax2_list]
        nr_vax2_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_vax2_list]
        nr_vax3_list = [0 if v<10 else v for v in nr_vax3_list]
        nr_vax3_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_vax3_list]

        nr_deaths_vax_list = [0 if v<10 else v for v in nr_deaths_vax_list]
        nr_deaths_novax_list = [0 if v<10 else v for v in nr_deaths_novax_list]

        nr_deaths_list = [0 if v<10 else v for v in nr_deaths_list]
        # nr_deaths_list = [int(round((float(v)/5.0),0)*5) if (v<=100 and v>10) else v for v in nr_deaths_list]
        # nr_deaths_list = [0 if v<10 else v for v in nr_deaths_list]
        # nr_deaths_covid_list = [0 if v<10 else v for v in nr_deaths_covid_list]
        nr_deaths_covid_list = [0 if v<10 else v for v in nr_deaths_covid_list]
        # nr_deaths_covid_list = [int(round((float(v)/5.0),0)*5) if (v<=100 and v>10) else v for v in nr_deaths_covid_list]

        nr_vaxed_alive_list = [0 if v<10 else v for v in nr_vaxed_alive_list]
        nr_vaxed_alive_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_vaxed_alive_list]
        # nr_vaxed_alive_list = [0 if v<10 else v for v in nr_vaxed_alive_list]
        # nr_unvaxed_alive_list = [0 if v<10 else v for v in nr_unvaxed_alive_list]
        nr_unvaxed_alive_list = [0 if v<10 else v for v in nr_unvaxed_alive_list]
        nr_unvaxed_alive_list = [int(round((float(v)/5.0),0)*5) if (v>10) else v for v in nr_unvaxed_alive_list]

        for idx, val in enumerate(nr_vaxed_alive_list):
            if val<10:
                nr_vaxed_alive_list[idx]=0
                # nr_deaths_vax_list[idx]=0
                perc_deaths_vax_list[idx]=0
                perc_deaths_vax_covid_list[idx]=0
                perc_deaths_vax_noncovid_list[idx]=0
                perc_U_vax_list[idx]=0
                perc_I_vax_list[idx]=0
                perc_C_vax_list[idx]=0
                perc_X_vax_list[idx]=0

        
        for idx, val in enumerate(nr_unvaxed_alive_list):
            if val<10:
                nr_unvaxed_alive_list[idx]=0
                # nr_deaths_novax_list[idx]=0
                perc_deaths_novax_list[idx]=0
                perc_deaths_novax_covid_list[idx]=0
                perc_deaths_novax_noncovid_list[idx]=0
                perc_U_unvax_list[idx]=0
                perc_I_unvax_list[idx]=0
                perc_C_unvax_list[idx]=0
                perc_X_unvax_list[idx]=0

        for idx, val in enumerate(nr_deaths_vax_list):
            if val<10:
                nr_deaths_vax_list[idx]=0
                perc_deaths_vax_list[idx]=0
                perc_deaths_vax_covid_list[idx]=0
                perc_deaths_vax_noncovid_list[idx]=0
                perc_U_vax_list[idx]=0
                perc_I_vax_list[idx]=0
                perc_C_vax_list[idx]=0
                perc_X_vax_list[idx]=0

        for idx, val in enumerate(nr_deaths_novax_list):
            if val<10:
                nr_deaths_novax_list[idx]=0
                perc_deaths_novax_list[idx]=0
                perc_deaths_novax_covid_list[idx]=0
                perc_deaths_novax_noncovid_list[idx]=0
                perc_U_unvax_list[idx]=0
                perc_I_unvax_list[idx]=0
                perc_C_unvax_list[idx]=0
                perc_X_unvax_list[idx]=0
                
        for idx, val in enumerate(nr_deaths_novax_list):
            val2 = nr_deaths_vax_list[idx]
            # if val==0 or val2==0:
            new_nr_deaths = val+val2
            perc_deaths_all_old = perc_deaths_all_list[idx]
            nr_deaths_all_old = float(nr_deaths_list[idx])
            nr_people_basedon = 0
            if perc_deaths_all_old>0:
                nr_people_basedon = nr_deaths_all_old*100/perc_deaths_all_old
            nr_deaths_list[idx]=new_nr_deaths
            if nr_people_basedon>0:
                perc_deaths_all_new = float(new_nr_deaths)/nr_people_basedon * 100
                perc_deaths_all_list[idx]=perc_deaths_all_new
                      
        
        for idx, val in enumerate(nr_deaths_covid_list):
            if val<10:
                nr_deaths_covid_list[idx]=0
                perc_deaths_covid_list[idx]=0
                perc_deaths_vax_covid_list[idx]=0
                perc_deaths_novax_covid_list[idx]=0
                perc_U_vax_list[idx]=0
                perc_U_unvax_list[idx]=0

        for idx, val in enumerate(nr_deaths_list):
            if val<10:
                nr_deaths_vax_list[idx]=0
                perc_deaths_vax_list[idx]=0
                perc_deaths_vax_covid_list[idx]=0
                perc_deaths_vax_noncovid_list[idx]=0
                nr_deaths_novax_list[idx]=0
                perc_deaths_novax_list[idx]=0
                perc_deaths_novax_covid_list[idx]=0
                perc_deaths_novax_noncovid_list[idx]=0
                nr_deaths_covid_list[idx]=0
                perc_deaths_covid_list[idx]=0
                perc_deaths_all_list[idx]=0
                perc_U_vax_list[idx]=0
                perc_I_vax_list[idx]=0
                perc_C_vax_list[idx]=0
                perc_X_vax_list[idx]=0
                perc_U_unvax_list[idx]=0
                perc_I_unvax_list[idx]=0
                perc_C_unvax_list[idx]=0
                perc_X_unvax_list[idx]=0


        if booster:
            nr_vax_list = nr_vax3_list
        else:
            nr_vax_list = nr_vax1_list
        for idx, val in enumerate(nr_vax_list):
            if val<10:
                if nr_vaxed_alive_list[idx]<10:
                    perc_vaccinated_list[idx]=0
                    nr_vaxed_alive_list[idx]=0
                    nr_deaths_vax_list[idx]=0
                    perc_deaths_vax_list[idx]=0
                    perc_deaths_vax_covid_list[idx]=0
                    perc_deaths_vax_noncovid_list[idx]=0
                    perc_U_vax_list[idx]=0
                    perc_I_vax_list[idx]=0
                    perc_C_vax_list[idx]=0
                    perc_X_vax_list[idx]=0
                    perc_U_unvax_list[idx]=0
                    perc_I_unvax_list[idx]=0
                    perc_C_unvax_list[idx]=0
                    perc_X_unvax_list[idx]=0

        eps = .001
        for idx, val in enumerate(perc_U_vax_list):
            perc_total = perc_U_vax_list[idx]+perc_I_vax_list[idx]+perc_C_vax_list[idx]+perc_X_vax_list[idx]
            if perc_total>eps and math.fabs(100-perc_total)>eps:
                perc_U_vax_list[idx] *= 100.0/perc_total
                perc_I_vax_list[idx] *= 100.0/perc_total
                perc_C_vax_list[idx] *= 100.0/perc_total
                perc_X_vax_list[idx] *= 100.0/perc_total
            perc_total = perc_U_unvax_list[idx]+perc_I_unvax_list[idx]+perc_C_unvax_list[idx]+perc_X_unvax_list[idx]
            if perc_total>eps and math.fabs(100-perc_total)>eps:
                perc_U_unvax_list[idx] *= 100.0/perc_total
                perc_I_unvax_list[idx] *= 100.0/perc_total
                perc_C_unvax_list[idx] *= 100.0/perc_total
                perc_X_unvax_list[idx] *= 100.0/perc_total

        # ****
        VE_RRR_maxval += .05*VE_RRR_maxval
        VE_RRR_minval -= .05*VE_RRR_minval
        VE_ARR_maxval += .05*VE_ARR_maxval
        VE_ARR_minval -= .05*VE_ARR_minval

        perc_deaths_minval = 0 -.05*perc_deaths_maxval

        fig,axs = plt.subplots(4,4) # , sharex=True

        # VACCINATIONS, POPULATION
        axs[0,0].plot(weeknr_list,nr_vax1_list, color = 'b', linestyle='solid', label='#1') #, label='vax 1 administered' , lw=2
        axs[0,0].plot(weeknr_list,nr_vax2_list, color = 'm', linestyle='solid', label='#2')
        axs[0,0].plot(weeknr_list,nr_vax3_list, color = 'y', linestyle='solid', label='#3')
        axs[0,0].legend()
        # axs[0,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[0,1].ylabel('number')
        axs[0,0].set(ylabel='number')
        # axs[0,0].set(xlabel='week number')
        axs[0,0].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[0,0].set_title('Vaccinations') #  (#1)
        axs[0,0].grid()

        # perc_vaccinated_list, nr_deaths_list
        axs[0,1].plot(weeknr_list,perc_vaccinated_list, color = 'b', linestyle='solid') #, label='vax 1 administered' , lw=2
        # axs[0,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[0,1].ylabel('number')
        axs[0,1].set(ylabel='%')
        # axs[0,0].set(xlabel='week number')
        axs[0,1].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[0,1].set_title('Vaccination rate')
        axs[0,1].set_ylim([-2,105])
        axs[0,1].grid()

        axs[0,2].plot(weeknr_list,nr_vaxed_alive_list, color = 'g', linestyle='solid', label='Vaccinated, alive') #, label='vax 1 administered' , lw=2
        axs[0,2].plot(weeknr_list,nr_unvaxed_alive_list, color = 'r', linestyle='solid', label='Unvaccinated, alive')
        axs[0,2].legend()
        axs[0,2].set(ylabel='number')
        axs[0,2].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[0,2].set_title('Vaccinated/unvaccinated population, alive')
        axs[0,2].grid()

        axs[0,3].plot(weeknr_list,nr_deaths_vax_list, color = 'g', linestyle='solid', label='Vaccinated, deaths')
        axs[0,3].plot(weeknr_list,nr_deaths_novax_list, color = 'r', linestyle='solid', label='Unvaccinated, deaths')
        axs[0,3].legend()
        axs[0,3].set(ylabel='number')
        axs[0,3].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[0,3].set_title('Number of dead, vaccinated/unvaccinated')
        axs[0,3].grid()

        # DEATHS PER 100K ***

        axs[1,0].plot(weeknr_list,nr_deaths_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,0].plot(weeknr_list,nr_deaths_list, color = 'b', linestyle='solid', label='ACM') #, label='vax 1 administered' , lw=2
        axs[1,0].plot(weeknr_list,nr_deaths_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,0].legend()
        # axs[0,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[0,1].ylabel('number')
        axs[1,0].set(ylabel='number')
        # axs[0,0].set(xlabel='week number')
        axs[1,0].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[1,0].set_title('Deaths counts')
        axs[1,0].grid()

        axs[1,1].plot(weeknr_list,perc_deaths_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,1].plot(weeknr_list,perc_deaths_all_list, color = 'b', linestyle='solid', label='ACM') # dotted, label='deaths all (per 100,000)' , lw=2
        axs[1,1].plot(weeknr_list,perc_deaths_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,1].legend()
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[1,1].set(ylabel='%')
        # axs[1,0].set(xlabel='week number')
        axs[1,1].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[1,1].set_title('Deaths all (%)')
        axs[1,1].set_ylim([perc_deaths_minval,perc_deaths_maxval])
        axs[1,1].grid()

        axs[1,2].plot(weeknr_list,perc_deaths_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,2].plot(weeknr_list,perc_deaths_vax_list, color = 'g', linestyle='solid', label='ACM') # , label='deaths vaccinated (per 100,000)'
        axs[1,2].plot(weeknr_list,perc_deaths_vax_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,2].legend()
        # axs[1,0].xticks(range(0, 52*nr_years + 2, 52))
        # axs[1,0].ylabel('deaths per 100,000')
        axs[1,2].set(ylabel='%')
        # axs[1,1].set(xlabel='week number')
        axs[1,2].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[1,2].set_title('Deaths vaccinated (%)')
        axs[1,2].set_ylim([perc_deaths_minval,perc_deaths_maxval])
        axs[1,2].grid()

        axs[1,3].plot(weeknr_list,perc_deaths_baseline_list, color = 'k', linestyle='solid', label='Normal')
        axs[1,3].plot(weeknr_list,perc_deaths_novax_list, color = 'r', linestyle='solid', label='ACM') # dashed, label='deaths unvaccinated (per 100,000)'
        axs[1,3].plot(weeknr_list,perc_deaths_novax_covid_list, color = 'c', linestyle='solid', label='Covid')
        axs[1,3].legend()
        # axs[1,1].xticks(range(0, 52*nr_years + 2, 52))
        # axs[1,1].ylabel('deaths per 100,000')
        axs[1,3].set(ylabel='%')
        # axs[1,2].set(xlabel='week number')
        axs[1,3].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[1,3].set_title('Deaths unvaccinated (%)')  
        axs[1,3].set_ylim([perc_deaths_minval,perc_deaths_maxval]) 
        axs[1,3].grid()
        
        # ** VE COVID / NON-COVID * 

        axs[2,0].plot([0, weeknr],[0, 0], color = 'k', linestyle='solid')
        axs[2,0].plot(weeknr_list,VE_RRR_covid_list, color = 'g', linestyle='solid') # dotted, label='deaths all (per 100,000)' , lw=2
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[2,0].set(ylabel='VE (%)')
        # axs[2,1].set(xlabel='week number')
        axs[2,0].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[2,0].set_title('VE RRR covid')
        axs[2,0].set_ylim([VE_RRR_minval,VE_RRR_maxval])
        axs[2,0].grid()

        axs[2,1].plot([0, weeknr],[0, 0], color = 'k', linestyle='solid')
        axs[2,1].plot(weeknr_list,VE_RRR_noncovid_list, color = 'g', linestyle='solid') # dotted, label='deaths all (per 100,000)' , lw=2
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[2,1].set(ylabel='VE (%)')
        # axs[2,2].set(xlabel='week number')
        axs[2,1].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[2,1].set_title('VE RRR non-covid')
        axs[2,1].set_ylim([VE_RRR_minval,VE_RRR_maxval])
        axs[2,1].grid()

    
        axs[2,2].plot([0, weeknr],[0, 0], color = 'k', linestyle='solid')
        axs[2,2].plot(weeknr_list,VE_ARR_covid_list, color = 'g', linestyle='solid') # dotted, label='deaths all (per 100,000)' , lw=2
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[2,2].set(ylabel='VE (% points)')
        # axs[3,1].set(xlabel='week number')
        axs[2,2].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[2,2].set_title('VE ARR covid')
        axs[2,2].set_ylim([VE_ARR_minval,VE_ARR_maxval])
        axs[2,2].grid()

        axs[2,3].plot([0, weeknr],[0, 0], color = 'k', linestyle='solid')
        axs[2,3].plot(weeknr_list,VE_ARR_noncovid_list, color = 'g', linestyle='solid') # dotted, label='deaths all (per 100,000)' , lw=2
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[2,3].set(ylabel='VE (% points)')
        # axs[3,2].set(xlabel='week number')
        axs[2,3].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[2,3].set_title('VE ARR non-covid')
        axs[2,3].set_ylim([VE_ARR_minval,VE_ARR_maxval])
        axs[2,3].grid()


        # ** VE ACM * 
        axs[3,0].plot([0, weeknr],[0, 0], color = 'k', linestyle='solid')
        axs[3,0].plot(weeknr_list,VE_RRR_ACM_list, color = 'g', linestyle='solid') # dotted, label='deaths all (per 100,000)' , lw=2
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[3,0].set(ylabel='VE (%)')
        # axs[2,0].set(xlabel='week number')
        axs[3,0].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[3,0].set_title('VE RRR ACM')
        axs[3,0].set_ylim([VE_RRR_minval,VE_RRR_maxval])
        axs[3,0].grid()

        axs[3,1].plot([0, weeknr],[0, 0], color = 'k', linestyle='solid')
        axs[3,1].plot(weeknr_list,VE_ARR_ACM_list, color = 'g', linestyle='solid') # dotted, label='deaths all (per 100,000)' , lw=2
        # axs[0,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[3,1].set(ylabel='VE (% points)')
        # axs[3,0].set(xlabel='week number')
        axs[3,1].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[3,1].set_title('VE ARR ACM')
        axs[3,1].set_ylim([VE_ARR_minval,VE_ARR_maxval])
        axs[3,1].grid()

        # perc_U_vax_list
        axs[3,2].plot(weeknr_list,perc_U_vax_list, color = 'c', linestyle='solid', label='U') 
        axs[3,2].plot(weeknr_list,perc_I_vax_list, color = 'r', linestyle='solid', label='I/R') 
        axs[3,2].plot(weeknr_list,perc_C_vax_list, color = 'b', linestyle='solid', label='C/D') 
        axs[3,2].plot(weeknr_list,perc_X_vax_list, color = 'g', linestyle='solid', label='Other') 
        axs[3,2].legend()
        # axs[,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[3,2].set(ylabel='%')
        # axs[2,0].set(xlabel='week number')
        axs[3,2].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[3,2].set_title('Causes of deaths (%), vaccinated')
        axs[3,2].set_ylim([-5,105])
        axs[3,2].grid()

        axs[3,3].plot(weeknr_list,perc_U_unvax_list, color = 'c', linestyle='solid', label='U') 
        axs[3,3].plot(weeknr_list,perc_I_unvax_list, color = 'r', linestyle='solid', label='I/R') 
        axs[3,3].plot(weeknr_list,perc_C_unvax_list, color = 'b', linestyle='solid', label='C/D') 
        axs[3,3].plot(weeknr_list,perc_X_unvax_list, color = 'g', linestyle='solid', label='Other') 
        axs[3,3].legend()
        # axs[,0].xticks(range(0, 52*nr_years + 2, 52))
        axs[3,3].set(ylabel='%')
        # axs[2,0].set(xlabel='week number')
        axs[3,3].set_xticks(range(0, 52*nr_years + 2, 13))
        axs[3,3].set_title('Causes of deaths (%), unvaccinated')
        axs[3,3].set_ylim([-5,105])
        axs[3,3].grid()

        # print()
        # print(VE_RRR_maxval)
        # print(VE_RRR_minval)
        # print()

        precision = 5
        precisionlow = 1
        precisionmed = 2

        perc_vaccinated_list = [f"{number:.{precisionlow}f}" for number in perc_vaccinated_list]
        perc_deaths_all_list = [f"{number:.{precision}f}" for number in perc_deaths_all_list]
        perc_deaths_covid_list = [f"{number:.{precision}f}" for number in perc_deaths_covid_list]
        perc_deaths_vax_covid_list = [f"{number:.{precision}f}" for number in perc_deaths_vax_covid_list]
        perc_deaths_vax_noncovid_list = [f"{number:.{precision}f}" for number in perc_deaths_vax_noncovid_list]
        perc_deaths_novax_covid_list = [f"{number:.{precision}f}" for number in perc_deaths_novax_covid_list]
        perc_deaths_novax_noncovid_list = [f"{number:.{precision}f}" for number in perc_deaths_novax_noncovid_list]
        perc_deaths_vax_list = [f"{number:.{precision}f}" for number in perc_deaths_vax_list]
        perc_deaths_novax_list = [f"{number:.{precision}f}" for number in perc_deaths_novax_list]

        VE_RRR_ACM_list = [f"{number:.{precisionmed}f}" for number in VE_RRR_ACM_list]
        VE_ARR_ACM_list = [f"{number:.{precision}f}" for number in VE_ARR_ACM_list]
        VE_RRR_covid_list = [f"{number:.{precisionmed}f}" for number in VE_RRR_covid_list]
        VE_ARR_covid_list = [f"{number:.{precision}f}" for number in VE_ARR_covid_list]
        VE_RRR_noncovid_list = [f"{number:.{precisionmed}f}" for number in VE_RRR_noncovid_list]
        VE_ARR_noncovid_list = [f"{number:.{precision}f}" for number in VE_ARR_noncovid_list]

        df_out = pd.DataFrame()
        df_out["weeknr_list"] = weeknr_list
        df_out["nr_vax1_list"] = nr_vax1_list
        df_out["nr_vax2_list"] = nr_vax2_list
        df_out["nr_vax3_list"] = nr_vax3_list
        df_out["perc_vaccinated_list"] = perc_vaccinated_list
        df_out["nr_vaxed_alive_list"] = nr_vaxed_alive_list
        df_out["nr_unvaxed_alive_list"] = nr_unvaxed_alive_list
        df_out["nr_deaths_vax_list"] = nr_deaths_vax_list
        df_out["nr_deaths_novax_list"] = nr_deaths_novax_list
        df_out["nr_deaths_list"] = nr_deaths_list
        df_out["nr_deaths_covid_list"] = nr_deaths_covid_list
        df_out["perc_deaths_all_list"] = perc_deaths_all_list
        df_out["perc_deaths_covid_list"] = perc_deaths_covid_list
        df_out["perc_deaths_vax_covid_list"] = perc_deaths_vax_covid_list
        df_out["perc_deaths_vax_noncovid_list"] = perc_deaths_vax_noncovid_list
        df_out["perc_deaths_novax_covid_list"] = perc_deaths_novax_covid_list
        df_out["perc_deaths_novax_noncovid_list"] = perc_deaths_novax_noncovid_list
        df_out["VE_RRR_ACM_list"] = VE_RRR_ACM_list
        df_out["VE_ARR_ACM_list"] = VE_ARR_ACM_list
        df_out["VE_RRR_covid_list"] = VE_RRR_covid_list
        df_out["VE_ARR_covid_list"] = VE_ARR_covid_list
        df_out["VE_RRR_noncovid_list"] = VE_RRR_noncovid_list
        df_out["VE_ARR_noncovid_list"] = VE_ARR_noncovid_list

        df_out["perc_U_vax_list"] = perc_U_vax_list
        df_out["perc_I_vax_list"] = perc_I_vax_list
        df_out["perc_C_vax_list"] = perc_C_vax_list
        df_out["perc_X_vax_list"] = perc_X_vax_list
        df_out["perc_U_unvax_list"] = perc_U_unvax_list
        df_out["perc_I_unvax_list"] = perc_I_unvax_list
        df_out["perc_C_unvax_list"] = perc_C_unvax_list
        df_out["perc_X_unvax_list"] = perc_X_unvax_list
        # nr_deaths_baseline_list, perc_deaths_baseline_list
        df_out["nr_deaths_baseline_list"] = nr_deaths_baseline_list
        df_out["perc_deaths_baseline_list"] = perc_deaths_baseline_list

        df_out["perc_deaths_vax_list"] = perc_deaths_vax_list
        df_out["perc_deaths_novax_list"] = perc_deaths_novax_list

        filename_csv = "H:/data/output/csv_python/ves/" + mat_str + "/ve_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + versionstr 
        if booster:
            filename_csv += "_BOOSTER"
        print("writing: "+filename_csv+ ".csv")
        df_out.to_csv(filename_csv+ ".csv")

        # plt.tight_layout()
        plt.subplots_adjust(hspace = 0.5)

        suptitle_str = "Age group " + str(birthyear_from) +"-" + str(birthyear_to) +", " + mat_str + versionstr +", WLZ " + str(wlz_bit) +", RxRisk LevelsType " + str(med_rxrisk_scores) + ", WLZ LevelsType " + str(wlz_levels) +", "+ yearsstr
        if booster:
            suptitle_str += ", BOOSTER"
        plt.suptitle(suptitle_str)
        manager = plt.get_current_fig_manager()
        # manager.window.state('zoomed')
        # # manager.window.showMaximized()
        manager.full_screen_toggle()
        
        # versionstr = "_v0"
        figfilestr = "H:/data/output/plots/ves/" + mat_str + "/ve_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + versionstr
        if booster:
            figfilestr += "_BOOSTER"
        plt.savefig(figfilestr + ".pdf", format="pdf", bbox_inches="tight")
        # plt.savefig("H:/data/plots/hist_deaths_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
        manager.full_screen_toggle()
        plt.show() # block=False

    return


