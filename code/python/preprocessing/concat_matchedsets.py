import os
import pandas as pd
import time
import argparse

def process_df(wlz_bit, med_rxrisk_bin, birthyear_from, birthyear_to, sex, versionstr, filename_core_prefix):
    basepath = "H:/data/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"

    filename_core = filename_core_prefix + str(birthyear_from) + "_" + str(birthyear_to) + "_Sex" + str(sex) + "_WLZ" + str(wlz_bit) + "_med_rxrisk_bin" + str(med_rxrisk_bin) + versionstr
    filename_ftr = basepath_ftr_matched+filename_core+".ftr"
    file_exists = os.path.exists(filename_ftr)
    
    df_part = None
    if file_exists:
        print(filename_ftr)
        print("reading: " + filename_core)
        df_part = pd.read_feather(filename_ftr)
        print(df_part.shape)
    
    return df_part


def run_main(birthyear_from_str, birthyear_to_str, wlz_bit_str):
    basepath = "H:/data/"
    basepath_ftr_matched = basepath+"python_pandas/matched/"
    basepath_csv_matched = basepath+"csv/matched/"

    # birthyear_from_total = 1930
    # birthyear_to_total = 1940
    # wlz_bit = 0
    birthyear_from_total = int(birthyear_from_str)
    birthyear_to_total = int(birthyear_to_str)
    wlz_bit = int(wlz_bit_str)

    stepsize_by = 5    
    versionstr = "_v3"
    print(versionstr)

    for file_type in range(3):
        if file_type == 0:
            filename_core_prefix = "matchedset_trackable_2021_"
        elif file_type == 1:
            filename_core_prefix = "notincludedset_trackable_2021_"
        elif file_type == 2:
            filename_core_prefix = "linkIDs_matched_trackable_2021_"
        print()
        print(filename_core_prefix)
        print()

        df_out = None
        for birthyear in range(birthyear_from_total,birthyear_to_total,stepsize_by):
            birthyear_from = birthyear
            birthyear_to = birthyear_from + stepsize_by
            for sex in range(1,3,1):
                if wlz_bit==0:
                    for med_rxrisk_bin in range(6): # (1,6,1)
                        df_part = process_df(wlz_bit, med_rxrisk_bin, birthyear_from, birthyear_to, sex, versionstr, filename_core_prefix)
                        if df_part is not None:
                            if df_out is None:
                                df_out = df_part
                            else:
                                df_out = pd.concat([df_out,df_part], ignore_index=True)   
                else:
                    med_rxrisk_bin = -1
                    df_part = process_df(wlz_bit, med_rxrisk_bin, birthyear_from, birthyear_to, sex, versionstr, filename_core_prefix)
                    if df_part is not None:
                        if df_out is None:
                            df_out = df_part
                        else:
                            df_out = pd.concat([df_out,df_part], ignore_index=True)   

        if df_out is not None:
            if filename_core_prefix != "linkIDs_matched_trackable_2021_":
                print("Sorting..")
                df_out.sort_values(by=["RINP_int"], inplace=True) # , "year", "yearweeknr"
                df_out.reset_index(inplace=True,drop=True)
                
            filename_core = filename_core_prefix + str(birthyear_from_total) + "_" + str(birthyear_to_total) + "_WLZ" + str(wlz_bit) + versionstr

            filename_csv = basepath_csv_matched+filename_core+"_head.csv"
            print("writing (head): "+filename_csv)
            df_out.head(1000).to_csv(filename_csv)

            filename_ftr = basepath_ftr_matched+filename_core+".ftr"
            print("writing: "+filename_ftr)
            df_out.to_feather(filename_ftr)


    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("birthyear_from_str")
    parser.add_argument("birthyear_to_str")
    parser.add_argument("wlz_bit_str")
    args = parser.parse_args()
    run_main(args.birthyear_from_str, args.birthyear_to_str, args.wlz_bit_str)
    