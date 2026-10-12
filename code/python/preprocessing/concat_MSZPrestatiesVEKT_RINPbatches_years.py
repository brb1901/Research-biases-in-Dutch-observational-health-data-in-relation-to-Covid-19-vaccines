import os
import pandas as pd
import time

def run_main():
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0"
    max_rinp_int_file = 1000000000 # 1 miljard
    firstyear = 2018
    lastyear = 2021

    # 

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
            filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + str(firstyear) + "_" + str(lastyear) + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
            filename_ftr = basepath_ftr + "multyears/" + filename_core + ".ftr" 
            file_exists = os.path.exists(filename_ftr)
            if not file_exists:
                df_out = None
                for year in [2018,2019,2020,2021]:
                    yearstr = str(year)
                    # print(year)
                    filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
                    filename_ftr = basepath_ftr + filename_core + ".ftr" 

                    file_exists = os.path.exists(filename_ftr)
                    if file_exists:
                        # print("reading " + filename_ftr)
                        df_indiv = pd.read_feather(filename_ftr)
                        # print(df_indiv.shape)
                        if year == firstyear:
                            df_out = df_indiv
                        else:
                            df_out = pd.concat([df_out,df_indiv], ignore_index=True)
                            # df_out.append(df_indiv)
                            df_out.reset_index(inplace=True,drop=True)
                
                if df_out is not None:
                    # print(df_out.shape)
                    # print(df_out)

                    filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + str(firstyear) + "_" + str(lastyear) + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
                    filename_ftr = basepath_ftr + "multyears/" + filename_core + ".ftr" 
                    print("writing: "+filename_ftr)
                    # start = time.time()
                    df_out.to_feather(filename_ftr)
                    # print(time.time() - start)
                    filename_csv = basepath_csv + "multyears/" + filename_core + "_head.csv"
                    print("writing: "+filename_csv)
                    df_out.head(100).to_csv(filename_csv)
                    print()
                else:
                    print("Empty df_out!")
            else:
                print(filename_core)
                print("exists already.")
    
    
if __name__ == '__main__':
    run_main()
    