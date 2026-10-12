import os
import pandas as pd
import re
import argparse

def run_main(year_string):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    basepath_comorb = "H:/data/csv/classcodes/" 
    filename_core = "classcodes_elixhauser"   
    print("reading " + filename_core + " csv data")
    df_comorb = pd.read_csv(basepath_comorb + filename_core + ".csv")
    comorb_vecsize = len(df_comorb["group"]) # 31
    print(comorb_vecsize)

    versionstr = "_v0"
    max_rinp_int_file = 1000000000 # 1 miljard

    year = int(year_string)
    # year = 2018
    # for year in [2018, 2019, 2020, 2021]:
    yearstr = str(year)
    print(year)

    use_cols = ['RINPERSOON',"year","quarter","file_ID_Prest","ICD10_list"]

    max_rinp_int = 0
    min_rinp_int = 1
    final_batch = False
    while (min_rinp_int <= max_rinp_int_file) and ~final_batch:
        min_rinp_int = max_rinp_int+1
        max_rinp_int = min_rinp_int-1 + 1000000 # 1000 #
        
        print(min_rinp_int)
        print(max_rinp_int)
        if min_rinp_int > max_rinp_int_file:
            final_batch = True
            print("Done!")
        else:
            filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_elixhauser_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
            filename_ftr = basepath_ftr + "elixhauser/" + filename_core + ".ftr" 
            file_exists = os.path.exists(filename_ftr)
            if not file_exists: # True: # not file_exists: # True: # 
                df_out = None
                # for year in [2018,2019,2020,2021]:
                #     yearstr = str(year)
                    # print(year)
                filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
                filename_ftr = basepath_ftr + filename_core + ".ftr" 

                file_exists = os.path.exists(filename_ftr)
                if file_exists:
                    print("reading " + filename_ftr)
                    df_indiv = pd.read_feather(filename_ftr)
                    # print(df_indiv.shape)
                    df_out = df_indiv.copy()
                    df_out = df_out[use_cols]
                    size = len(df_indiv["RINPERSOON"])

                    score = [float(0)] * size # baselist
                    catlist = []
                    for j in range(comorb_vecsize):
                        catlist.append([])
                        catlist[j] = [int(0)] * size # baselist

                    for index, rowdata in df_indiv.iterrows():
                        if index % 10000 == 0:
                            print(index)
                        ICD10_list_str = rowdata["ICD10_list"]  
                        score_total =  0 
                        if ICD10_list_str:                      
                            # score_this =  0
                            for index_comorb, rowdata_comorb in df_comorb.iterrows():
                            # for j in range(comorb_vecsize):
                                regex_str = rowdata_comorb["regex_icd10"]
                                match_regex = re.search(regex_str, ICD10_list_str)
                                if match_regex:
                                    score_this = rowdata_comorb["index_sum_all"]
                                    catlist[index_comorb][index] = score_this
                                    score_total +=  score_this
                                    # print(rowdata["RINPERSOON"])
                                    # print(ICD10_list_str)
                                    # print(regex_str)
                                    # # #DEBUG
                                    # exit(1)

                        score[index] = score_total

                    # print(cat)
                    df_out["score"] = score
                    for j in range(comorb_vecsize):
                        catsubstr = "cat" + str(j)
                        df_out[catsubstr] = catlist[j]
                else:
                    print("File does not exist!")
                
                if df_out is not None:
                    # print(df_out.shape)
                    # print(df_out)

                    filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_elixhauser_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
                    filename_ftr = basepath_ftr + "elixhauser/" + filename_core + ".ftr" 
                    print("writing: "+filename_ftr)
                    # start = time.time()
                    df_out.to_feather(filename_ftr)
                    # print(time.time() - start)
                    filename_csv = basepath_csv + "elixhauser/" + filename_core + "_head.csv"
                    print("writing: "+filename_csv)
                    df_out.head(100).to_csv(filename_csv)
                    print()
                else:
                    print("Empty df_out!")

                # #DEBUG
                # exit(1)
            else:
                print(filename_core)
                print("exists already.")
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year_string")
    args = parser.parse_args()
    run_main(args.year_string)
    