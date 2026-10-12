import pandas as pd
import time
import argparse
# from datetime import date
# import gc
# import math
# import os

def run_main(birthyear_from_str, birthyear_to_str):
    basepath = "H:/data/"
    # basepath_ftr = basepath+"python_pandas/GBA/"
    # basepath_csv = basepath+"csv/GBA/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    basepath_csv_matched = basepath+"csv/matched/"

    versionstr = "_v0"
    r_seed = 0
    nr_extratreated_req = 2
    stepsize_by = 5
 
    # stepsize = 10
    # birthyear_from = 1930
    # birthyear_to = birthyear_from + stepsize
    birthyear_from_total = int(birthyear_from_str)
    birthyear_to_total = int(birthyear_to_str)

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
        for sex in range(1,3,1):
            for wlz_bit in range(2):
                print(str(birthyear_from) + "-" + str(birthyear_to))
                print("Sex: " + str(sex))
                print("WLZ: " + str(wlz_bit))
                df_p = df_pt.copy()
                df_p = df_p[( (df_p['GBAGEBOORTEJAAR']>=birthyear_from) & (df_p['GBAGEBOORTEJAAR']<birthyear_to) 
                               & (df_p['GBAGESLACHT']==str(sex)) & (df_p['WLZ_bit']==wlz_bit) )] 
                df_p.reset_index(inplace=True,drop=True)
                print(df_p.shape)
                nr_total = len(df_p)
                print(nr_total)

                # exit(1)

                df_p["included"] = 0
                df_p["excluded"] = 0
                df_p["linkID"] = -1
                df_p["start_date"] = None
                df_p["treatment"] = 0
                df_p["control"] = 0

                linkID_list = []
                target_treated_list = []
                matched_treated_list = []
                matched_control_list = []

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
                while eligible_found: # and match_found:  # nr_eligible>0: 
                    m0 = ( (df_p["included"]==0) & (df_p["excluded"]==0) & (df_p["vaccinated_bit"]==1) )
                    # eligible_found = False
                    # match_found = False
                    for index, row in df_p.loc[m0].iterrows():   # the first one here is vaxed0, our target to match to
                        # if linkID>linkID_prev and linkID % 100 == 0 and linkID!=0:
                        # if index % 1000 == 0 and index!=0:
                        if (index - index_prev) >= 1000: # == 0 and index!=0:
                            print(str(birthyear_from_total) + "-" + str(birthyear_to_total))
                            print(str(birthyear_from) + "-" + str(birthyear_to))
                            print("Sex: " + str(sex))
                            print("WLZ: " + str(wlz_bit))
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
                        if df_p.iloc[index]["included"]==0 and df_p.iloc[index]["excluded"]==0:
                            eligible_found = True
                            target_rinpersoon =  df_p.iloc[index]["RINPERSOON"]
                            target_week_nr = df_p.iloc[index]["week_nr_firstvax"]
                            target_birthyear_bin = df_p.iloc[index]["GBAGEBOORTEJAAR_bin"]
                            target_start_date = df_p.iloc[index]["covid_vax_firstdate"]
                            if wlz_bit:
                                target_WLZ_type = df_p.iloc[index]["WLZ_type"]
                                target_WLZ_level = df_p.iloc[index]["WLZ_level"]
                            else:
                                target_comorb_score0_bin = df_p.iloc[index]["med_rxrisk_score_weightedpratt_prevyear_bin"]

                            # find matched TREATED (vaccinated):
                            if wlz_bit:
                                m1 = ( (df_p["included"]==0) & (df_p["excluded"]==0) & (df_p["vaccinated_bit"]==1)
                                    & (df_p["RINPERSOON"]!=target_rinpersoon) 
                                    & (df_p["week_nr_firstvax"]==target_week_nr) & (df_p["GBAGEBOORTEJAAR_bin"]==target_birthyear_bin) 
                                    & (df_p["WLZ_type"]==target_WLZ_type) & (df_p["WLZ_level"]==target_WLZ_level) )
                            else:
                                m1 = ( (df_p["included"]==0) & (df_p["excluded"]==0) & (df_p["vaccinated_bit"]==1)
                                    & (df_p["RINPERSOON"]!=target_rinpersoon) 
                                    & (df_p["week_nr_firstvax"]==target_week_nr) & (df_p["GBAGEBOORTEJAAR_bin"]==target_birthyear_bin) 
                                    & (df_p["med_rxrisk_score_weightedpratt_prevyear_bin"]==target_comorb_score0_bin) )
                                
                            nr_treated_matched = 0
                            enough_treated_matched = False           
                            # index1_list = []
                            for index1, row1 in df_p.loc[m1].iterrows():   # the first one here is vaxed1, the second one is vaxed2
                                # index1_list.append(index1)
                                nr_treated_matched += 1
                                if nr_treated_matched==nr_extratreated_req:
                                    enough_treated_matched=True
                                    break
                            
                            enough_control_matched = False
                            if enough_treated_matched:
                                # find matched CONTROL (UNvaccinated):
                                if wlz_bit:
                                    m2 = ( (df_p["included"]==0) & (df_p["excluded"]==0) & (df_p["vaccinated_bit"]==0)
                                        & (df_p["GBAGEBOORTEJAAR_bin"]==target_birthyear_bin) 
                                        & (df_p["WLZ_type"]==target_WLZ_type) & (df_p["WLZ_level"]==target_WLZ_level) 
                                        & ( (df_p["dead_bit"]==0) | ((df_p["dead_bit"]==1) & (df_p["dead_date"]>target_start_date)) ) )
                                else:
                                    m2 = ( (df_p["included"]==0) & (df_p["excluded"]==0) & (df_p["vaccinated_bit"]==0)
                                        & (df_p["GBAGEBOORTEJAAR_bin"]==target_birthyear_bin) 
                                        & (df_p["med_rxrisk_score_weightedpratt_prevyear_bin"]==target_comorb_score0_bin)
                                        & ( (df_p["dead_bit"]==0) | ((df_p["dead_bit"]==1) & (df_p["dead_date"]>target_start_date)) ) )
                                    
                                nr_control_matched = 0
                                # matched_treated_rinpersoon = []
                                # index2_list = []
                                for index2, row2 in df_p.loc[m2].iterrows():   # the first one here is unvaxed0
                                    # index2_list.append(index2)
                                    nr_control_matched += 1
                                    if nr_control_matched==1:
                                        enough_control_matched=True
                                        break

                            if enough_treated_matched and enough_control_matched:
                                # vaxed0:
                                df_p.at[index,"linkID"]=linkID
                                df_p.at[index,"included"]=1
                                df_p.at[index,"treatment"]=1
                                df_p.at[index,"start_date"]=target_start_date

                                matched_treated_rinpersoon = []
                                nr_treated_matched = 0
                                for index1, row1 in df_p.loc[m1].iterrows():   # the first one here is vaxed1, the second one is vaxed2
                                    df_p.at[index1,"linkID"]=linkID
                                    df_p.at[index1,"included"]=1
                                    df_p.at[index1,"treatment"]=1
                                    treatedmatched_start_date = df_p.iloc[index1]["covid_vax_firstdate"]
                                    df_p.at[index1,"start_date"]=treatedmatched_start_date
                                    matched_rinpersoon =  df_p.iloc[index1]["RINPERSOON"]
                                    matched_treated_rinpersoon.append(matched_rinpersoon)
                                    # index1_list.append(index1)
                                    nr_treated_matched += 1
                                    if nr_treated_matched==nr_extratreated_req:
                                        break

                                nr_control_matched = 0
                                matched_control_rinpersoon = "" # []
                                for index2, row2 in df_p.loc[m2].iterrows():   # the first one here is unvaxed0
                                    df_p.at[index2,"linkID"]=linkID
                                    df_p.at[index2,"included"]=1
                                    df_p.at[index2,"control"]=1
                                    df_p.at[index2,"start_date"]=target_start_date
                                    matched_rinpersoon =  df_p.iloc[index2]["RINPERSOON"]
                                    # matched_control_rinpersoon.append(matched_rinpersoon)
                                    matched_control_rinpersoon = matched_rinpersoon
                                    # index2_list.append(index2)
                                    nr_control_matched += 1
                                    if nr_control_matched==1:
                                        break

                                linkID_list.append(linkID)
                                target_treated_list.append(target_rinpersoon)
                                matched_treated_rinpersoon_str = ';'.join(map(str,matched_treated_rinpersoon))
                                matched_treated_list.append(matched_treated_rinpersoon_str)
                                matched_control_list.append(matched_control_rinpersoon)
                                # match_found = True
                                # print("matched:")
                                # print(linkID)
                                # print(target_rinpersoon)
                                # print(matched_treated_rinpersoon_str)
                                # print(matched_control_rinpersoon)
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
                    eligible_found = False

                #DEBUG
                # exit(1)

                print()

                # print("*** DEBUG SKIPPING Sorting..")
                print("Sorting..")
                # df_uniquepeople.sort_values(by=["RINPERSOON"], inplace=True) # , "year", "yearweeknr"
                df_p.sort_values(by=["RINP_int"], inplace=True) # , "year", "yearweeknr"
                df_p.reset_index(inplace=True,drop=True)

                versionstr = "_v2"

                if len(linkID_list):
                    df_linkID = pd.DataFrame()
                    df_linkID["linkID"] = linkID_list
                    df_linkID["target_treated"] = target_treated_list
                    df_linkID["matched_treated"] = matched_treated_list
                    df_linkID["matched_control"] = matched_control_list

                    filename_core = "linkIDs_matched_trackable_2021_" + str(birthyear_from) + "_" + str(birthyear_to) + "_Sex" + str(sex) + "_WLZ" + str(wlz_bit) + versionstr

                    filename_csv = basepath_csv_matched+filename_core+"_head.csv"
                    print("writing (head): "+filename_csv)
                    # start = time.time()
                    df_linkID.head(1000).to_csv(filename_csv)
                    # print(time.time() - start)

                    filename_ftr = basepath_ftr_matched+filename_core+".ftr"
                    print("writing: "+filename_ftr)
                    # start = time.time()
                    df_linkID.to_feather(filename_ftr)
                    # print(time.time() - start)


                print("Selecting included..")
                df_p_sel = df_p[ (df_p['included']==1) ]
                df_p_sel.reset_index(inplace=True,drop=True)
                print(df_p.shape)

                print()

                # versionstr = "_v0B"
                filename_core = "matchedset_trackable_2021_" + str(birthyear_from) + "_" + str(birthyear_to) + "_Sex" + str(sex) + "_WLZ" + str(wlz_bit) + versionstr

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

                print()
                print("Selecting not-included..")
                df_p_sel = df_p[ (df_p['included']==0) ]
                df_p_sel.reset_index(inplace=True,drop=True)
                print(df_p.shape)

                print()

                # versionstr = "_v0B"
                filename_core = "notincludedset_trackable_2021_" + str(birthyear_from) + "_" + str(birthyear_to) + "_Sex" + str(sex) + "_WLZ" + str(wlz_bit) + versionstr

                filename_csv = basepath_csv_matched+filename_core+"_head.csv"
                print("writing (head): "+filename_csv)
                # start = time.time()
                df_p_sel.head(1000).to_csv(filename_csv)
                # print(time.time() - start)

                filename_ftr = basepath_ftr_matched+filename_core+".ftr"
                print("writing: "+filename_ftr)
                # start = time.time()
                df_p_sel.to_feather(filename_ftr)

    print("Total processing time: ")
    print(time.time() - start_overall)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("birthyear_from_str")
    parser.add_argument("birthyear_to_str")
    # parser.add_argument("wlz_bit_str")
    args = parser.parse_args()
    run_main(args.birthyear_from_str, args.birthyear_to_str)


    