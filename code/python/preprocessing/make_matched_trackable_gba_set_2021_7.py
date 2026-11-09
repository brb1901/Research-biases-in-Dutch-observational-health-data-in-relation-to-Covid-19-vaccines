import pandas as pd
import time
import argparse
from datetime import datetime # date, 
# import gc
# import math
import os

# DIT IS DE OVERALL DATASET! Dwz random gesampled, zowel gevaccineerden als ongevaccineerden, volgens verhouding in de populatie.

def process_df(df_ps, wlz_bit, birthyear_from, birthyear_to):
    basepath = "H:/data/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    basepath_csv_matched = basepath+"csv/matched/"

    versionstr = "_v7" # "_v3"
    filename_core = "matchedset_trackable_2021_overallrandom_" + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit)  + versionstr
    filename_ftr = basepath_ftr_matched+filename_core+".ftr"
    file_exists = os.path.exists(filename_ftr)
    
    if file_exists:
        print(filename_ftr)
        print("File exists already! Skipping.")
    else:        
        df_p = df_ps.copy()
        df_p.reset_index(inplace=True,drop=True)
        print(df_p.shape)
        nr_total = len(df_p)
        # print(nr_total)

        print(str(birthyear_from) + "-" + str(birthyear_to))
        # print("Sex: " + str(sex))
        print("WLZ: " + str(wlz_bit))
        # print("med_rxrisk_bin: " + str(med_rxrisk_bin))
        print("Total: " + str(nr_total))

        if nr_total>0:
            df_p["included"] = 0
            df_p["excluded"] = 0
            df_p["linkID"] = -1
            df_p["start_date"] = None
            df_p["treatment"] = 0
            df_p["control"] = 0

            # linkID_list = []
            # target_treated_list = []
            # matched_treated_list = []
            # matched_control_list = []

            print()
            print("Processing..")
            print()
            # nr_eligible = 1
            eligible_found = True 
            # match_found = True
            linkID = 0
            # linkID_prev=-100
            nr_excluded = 0
            start = time.time()
            index_prev = 0

            if wlz_bit:
                overall_start_date = datetime(2021,1,1,0,0,0)
            else:
                overall_start_date = datetime(2021,2,20,0,0,0)
            prev_vax_start_date = overall_start_date
            # nr_extra_req = 1
            max_number = 400000

            while eligible_found and linkID<max_number: # and match_found:  # nr_eligible>0: 
                m0 = ( (df_p["included"]==0) & (df_p["excluded"]==0) & ( (df_p["dead_bit"]==0) | ((df_p["dead_bit"]==1) & (df_p["dead_date"]>overall_start_date)) ) ) #  & (df_p["vaccinated_bit"]==1) 
                # eligible_found = False
                # match_found = False
                for index, row in df_p.loc[m0].iterrows():   # the first one here is our target to match to
                    # if linkID>linkID_prev and linkID % 100 == 0 and linkID!=0:
                    # if index % 1000 == 0 and index!=0:
                    if (index - index_prev) >= 1000: # == 0 and index!=0:
                        # print(str(birthyear_from_total) + "-" + str(birthyear_to_total))
                        print(str(birthyear_from) + "-" + str(birthyear_to))
                        # print("Sex: " + str(sex))
                        print("WLZ: " + str(wlz_bit))
                        # print("med_rxrisk_bin: " + str(med_rxrisk_bin))
                        print("Total: " + str(nr_total))
                        print(index)
                        print(linkID)                            
                        df_sel = df_p[ (df_p['included']==1) | (df_p['excluded']==1) ]
                        print("Included and excluded so far: " + str(len(df_sel)))
                        print("Explicitly excluded so far: " + str(nr_excluded))
                        print(time.time() - start)
                        start = time.time()
                        index_prev = index
                        print()
                    
                    eligible_found = False
                    if df_p.iloc[index]["included"]==0 and df_p.iloc[index]["excluded"]==0: # (vaccinated OR unvaccinated)
                        eligible_found = True
                        # target_rinpersoon =  df_p.iloc[index]["RINPERSOON"]

                        target_start_date = overall_start_date

                        if df_p.iloc[index]["vaccinated_bit"]==1: # vaccinated person
                            # target_week_nr = df_p.iloc[index]["week_nr_firstvax"]
                            # target_birthyear_bin = df_p.iloc[index]["GBAGEBOORTEJAAR_bin"]
                            target_start_date = df_p.iloc[index]["covid_vax_firstdate"]
                            prev_vax_start_date = target_start_date
                        else: # unvaccinated person
                            # prev_vax_start_date
                            if df_p.iloc[index]["dead_bit"]==0 | ((df_p.iloc[index]["dead_bit"]==1) & (df_p.iloc[index]["dead_date"]>prev_vax_start_date) ):
                                target_start_date = prev_vax_start_date
                            else:
                                target_start_date = overall_start_date
                        
                        # if wlz_bit:
                        #     target_WLZ_type = df_p.iloc[index]["WLZ_type"]
                        #     target_WLZ_level = df_p.iloc[index]["WLZ_level"]

                        enough_treated_matched=True
                        enough_control_matched=True

                        if enough_treated_matched and enough_control_matched:
                            # vaxed0:
                            df_p.at[index,"linkID"]=linkID
                            df_p.at[index,"included"]=1
                            df_p.at[index,"treatment"]=df_p.at[index,"vaccinated_bit"]
                            df_p.at[index,"start_date"]=target_start_date

                            linkID += 1
                            #DEBUG
                            # if linkID>1002:
                            #     eligible_found = False
                            #     break
                        else:
                            df_p.at[index,"excluded"]=1
                            nr_excluded += 1
                            # print("not matched:")
                            # print(target_rinpersoon)
                        
                        if linkID>=max_number:
                            break
                eligible_found = False

            #DEBUG
            # exit(1)

            # print()

            # print("*** DEBUG SKIPPING Sorting..")
            print("Sorting..")
            # df_uniquepeople.sort_values(by=["RINPERSOON"], inplace=True) # , "year", "yearweeknr"
            df_p.sort_values(by=["RINP_int"], inplace=True) # , "year", "yearweeknr"
            df_p.reset_index(inplace=True,drop=True)

            # if len(linkID_list):
            #     df_linkID = pd.DataFrame()
            #     df_linkID["linkID"] = linkID_list
            #     df_linkID["target_treated"] = target_treated_list
            #     df_linkID["matched_treated"] = matched_treated_list
            #     df_linkID["matched_control"] = matched_control_list

            #     filename_core = "linkIDs_matched_trackable_2021_" + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr

            #     filename_csv = basepath_csv_matched+filename_core+"_head.csv"
            #     print("writing (head): "+filename_csv)
            #     # start = time.time()
            #     df_linkID.head(1000).to_csv(filename_csv)
            #     # print(time.time() - start)

            #     filename_ftr = basepath_ftr_matched+filename_core+".ftr"
            #     print("writing: "+filename_ftr)
            #     # start = time.time()
            #     df_linkID.to_feather(filename_ftr)
            #     # print(time.time() - start)


            print("Selecting included..")
            df_p_sel = df_p[ (df_p['included']==1) ]
            df_p_sel.reset_index(inplace=True,drop=True)
            print(df_p_sel.shape)

            print()

            # versionstr = "_v0B"
            filename_core = "matchedset_trackable_2021_overallrandom_" + str(birthyear_from) + "_" + str(birthyear_to) + "_WLZ" + str(wlz_bit) + versionstr

            filename_csv = basepath_csv_matched+filename_core+"_head.csv"
            print("writing (head): "+filename_csv)
            # start = time.time()
            df_p_sel.head(1000).to_csv(filename_csv)
            # print(time.time() - start)

            filename_ftr = basepath_ftr_matched+filename_core+".ftr"
            print("writing: "+filename_ftr)
            # start = time.time()
            df_p_sel.to_feather(filename_ftr)
            # print(time.time() - start)

            # print()
            # print("Selecting not-included..")
            # df_p_sel = df_p[ (df_p['included']==0) ]
            # df_p_sel.reset_index(inplace=True,drop=True)
            # print(df_p_sel.shape)

            # print()

            # # versionstr = "_v0B"
            # filename_core = "notincludedset_trackable_2021_" + str(birthyear_from) + "_" + str(birthyear_to) + "_Sex" + str(sex) + "_WLZ" + str(wlz_bit) + "_med_rxrisk_bin" + str(med_rxrisk_bin) + versionstr

            # filename_csv = basepath_csv_matched+filename_core+"_head.csv"
            # print("writing (head): "+filename_csv)
            # # start = time.time()
            # df_p_sel.head(1000).to_csv(filename_csv)
            # # print(time.time() - start)

            # filename_ftr = basepath_ftr_matched+filename_core+".ftr"
            # print("writing: "+filename_ftr)
            # # start = time.time()
            # df_p_sel.to_feather(filename_ftr)

    print()


def run_main(birthyear_from_str, birthyear_to_str):
    basepath = "H:/data/"
    # basepath_ftr = basepath+"python_pandas/GBA/"
    # basepath_csv = basepath+"csv/GBA/"
    

    versionstr = "_v0"
    r_seed = 1 # 0
    # nr_extratreated_req = 2
 
    # stepsize = 10
    # birthyear_from = 1930
    # birthyear_to = birthyear_from + stepsize
    birthyear_from_total = int(birthyear_from_str)
    birthyear_to_total = int(birthyear_to_str)

    stepsize_by = birthyear_to_total - birthyear_from_total    # **** 10; NOW CHANGED SO I CAN JUST RUN 1960-1980 in ONE GO!

    filename_core = "GBAPERSOON_trackable_2021_SESWOA_WLZ_ComorbMed_Dead_Vax_Bins_CNCdead" + versionstr
    print("reading: " + filename_core)
    df_pt = pd.read_feather(basepath+"python_pandas/GBA/" + filename_core +".ftr")
    print(df_pt.shape)

    print("Selecting subpopulation for matching..")
    print(str(birthyear_from_total) + "-" + str(birthyear_to_total) )
    df_pt = df_pt[( (df_pt['GBAGEBOORTEJAAR']>=birthyear_from_total) & (df_pt['GBAGEBOORTEJAAR']<birthyear_to_total) ) ] # & (df_p['WLZ_bit']==wlz_bit)
    df_pt.reset_index(inplace=True,drop=True)
    print(df_pt.shape)
    print(len(df_pt))

    print("Making int RINP_int..")
    df_pt["RINP_int"] = df_pt["RINPERSOON"].astype(int)

    print("Random shuffling..")
    df_pt = df_pt.sample(frac=1, random_state=r_seed) #.reset_index(inplace=True,drop=True)
    df_pt.reset_index(inplace=True,drop=True)
    print(df_pt.shape)
    print(len(df_pt))
    print()
    start_overall = time.time()

    # print(df_pt.head())

    for birthyear in range(birthyear_from_total,birthyear_to_total,stepsize_by):
        birthyear_from = birthyear
        birthyear_to = birthyear_from + stepsize_by
        # for sex in range(1,3,1):
        for wlz_bit in [0]:    #  range(2):   # [1]: #  ********   range(2):
            print(str(birthyear_from) + "-" + str(birthyear_to))
            # print("Sex: " + str(sex))
            print("WLZ: " + str(wlz_bit))
            df_p = df_pt.copy()
            df_p = df_p[( (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) 
                         & (df_p['WLZ_bit']==wlz_bit) )] 
            # df_pr = df_p
            
            # med_rxrisk_bin_val = df_p['med_rxrisk_score_weightedpratt_prevyear_bin'].max()
            # print(med_rxrisk_bin_val)
            # med_rxrisk_bin_val = df_p['med_rxrisk_score_weightedpratt_prevyear_bin'].min()
            # print(med_rxrisk_bin_val)
            
            # if wlz_bit==0:
            #     for med_rxrisk_bin in range(6): # (1,6,1)
            #         df_p = df_pr.copy()
            #         df_p = df_p[( (df_p['med_rxrisk_score_weightedpratt_prevyear_bin']==med_rxrisk_bin) )] 
            #         process_df(df_p, wlz_bit, med_rxrisk_bin, birthyear_from, birthyear_to, nr_extratreated_req, sex)
            # else:
                # med_rxrisk_bin = -1
                
            process_df(df_p, wlz_bit, birthyear_from, birthyear_to)

                # exit(1)      

    print("Total processing time: ")
    print(time.time() - start_overall)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("birthyear_from_str")
    parser.add_argument("birthyear_to_str")
    # parser.add_argument("wlz_bit_str")
    args = parser.parse_args()
    run_main(args.birthyear_from_str, args.birthyear_to_str)


    