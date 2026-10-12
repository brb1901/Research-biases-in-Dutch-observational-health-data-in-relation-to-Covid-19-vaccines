import os
import pandas as pd
import time
import argparse
from datetime import date, datetime, timedelta
import gc


def select_cols(df, usecols):
    if usecols is not None:
        print("selecting columns")
        df2 = df[usecols]
        df.iloc[0:0]
        del df
        gc.collect()
        df = df2
        df2.iloc[0:0]
        del df2
        gc.collect()
    return df

def read_make_compact_df_pres(filename, use_cols):
    print("reading " + filename)
    start = time.time()    
    df_pres = pd.read_feather(filename)
    print(time.time() - start)
    # print(df_pres.shape)
    df_pres["RINP_int"] = df_pres["RINPERSOON"].astype(int)
    df_pres["datetimeobj_begin"] = pd.to_datetime(df_pres["VEKTMSZBegindatumPrest"])
    df_pres = select_cols(df_pres, use_cols)
    return df_pres


def parse_dbc_string(dbc):
    dbc_list = dbc.split('-')
    aaaa = (dbc_list[0])
    dddd = (dbc_list[3])
    return [aaaa, dddd]


def run_main(year_string, i_cc_string):
    basepath = "H:/data/"
    basepath_ftr_vektis = basepath+"python_pandas/VEKTIS/"
    basepath_csv_vektis = basepath + "csv/VEKTIS/"

    # firstyear = 2018
    # lastyear = 2021
    versionstr = "_v0"  #"_v0_test" 
    year = int(year_string)
    yearstr = str(year)
    print(year)
    print()

    # use_cols = ['RINPERSOON','datetimeobj_begin','RINP_int','VEKTMSZKoppelIDPrestZa','VEKTMSZZorgtype',
    #             'VEKTMSZSpecialismeDiagnoseCombinatie'] # "VEKTMSZBegindatumPrest" 
    use_cols = ['RINPERSOON','datetimeobj_begin','RINP_int',
                'VEKTMSZSpecialismeDiagnoseCombinatie'] # "VEKTMSZBegindatumPrest" 
    print()
    
    start_proc = time.time() 
    
    i_cc = int(i_cc_string) # 0
    
    while i_cc <= 100:
        df_out = pd.DataFrame() #None
        # pers_i = 0
        # special_case_end_file = False
        filename_core = "MSZPrestatiesVEKT" + yearstr + "_cc_" + str(i_cc) + ".ftr" # "_total.ftr" "_cc_
        filename = basepath_ftr_vektis + filename_core
        df_in = read_make_compact_df_pres(filename, use_cols)

        min_rinp_int_file = df_in["RINP_int"].min()
        print("min_rinp_int_file")
        print(min_rinp_int_file)
        max_rinp_int_file = df_in["RINP_int"].max()
        print("max_rinp_int_file")
        print(max_rinp_int_file)

        rinp_ser = df_in["RINPERSOON"].unique()
        # rinp_ser = df_uniquepeople_pres["RINPERSOON"].unique()
        nr_rinp = len(rinp_ser)
        print("Number of people to handle in this batch:")
        print(nr_rinp)
        
        rinp_list = []
        dbc_list = []
        specialism_list = []
        datetimeobj_list = []

        start = time.time()
        for index, rowdata in df_in.iterrows():
            if index % 1000000 == 0:
                print(index)
                print(rowdata)          
                print(time.time() - start)
                start = time.time()
                print()
                # if len(rinp_list):
                #     break
            
            dbc = rowdata["VEKTMSZSpecialismeDiagnoseCombinatie"]
            # aaaa = ""
            # dddd = ""
            if dbc != "9999-99-99-9999":
                [aaaa, dddd] = parse_dbc_string(dbc)
                if aaaa == "0320" or aaaa == "0316" or aaaa == "0313" or aaaa == "8416":
                    rinp = rowdata["RINPERSOON"]
                    datetimeobj_begin = rowdata["datetimeobj_begin"]
                    if aaaa == "0320":
                        rinp_list.append(rinp)
                        dbc_list.append(dbc)
                        specialism_list.append(aaaa)
                        datetimeobj_list.append(datetimeobj_begin)
                    elif aaaa == "0316":
                        dddd_int = int(dddd)
                        if dddd == "1405" or dddd == "1703" or dddd == "1704" or dddd == "1707" or dddd == "1799" or dddd_int >= 3401 and dddd_int <= 3501:
                            rinp_list.append(rinp)
                            dbc_list.append(dbc)
                            specialism_list.append(aaaa)
                            datetimeobj_list.append(datetimeobj_begin)
                    elif aaaa == "0313":
                        dddd_int = int(dddd)
                        if dddd_int >= 101 and dddd_int <= 141:
                            rinp_list.append(rinp)
                            dbc_list.append(dbc)
                            specialism_list.append(aaaa)
                            datetimeobj_list.append(datetimeobj_begin)
                    elif aaaa == "8416":
                        dddd_int = int(dddd)
                        if dddd_int >= 101 and dddd_int <= 199:
                            rinp_list.append(rinp)
                            dbc_list.append(dbc)
                            specialism_list.append(aaaa)
                            datetimeobj_list.append(datetimeobj_begin)

        df_out["RINPERSOON"] = rinp_list
        df_out["dbc"] = dbc_list
        df_out["specialism"] = specialism_list
        df_out["datetime"] = datetimeobj_list
        df_out.reset_index(inplace=True,drop=True)

        print(df_out.shape)
        filename_core =  "selectedpeople_VektPrest_HeartDiag_" + yearstr + "_cc_" + str(i_cc) + versionstr
        filename_ftr = basepath_ftr_vektis + "selection_zorgpaden/" + filename_core + ".ftr" 
        print("writing: "+filename_ftr)
        start = time.time()
        df_out.to_feather(filename_ftr)
        print(time.time() - start)
        filename_csv = basepath_csv_vektis + "selection_zorgpaden/" + filename_core + "_head.csv"
        print("writing: "+filename_csv)
        df_out.head(1000).to_csv(filename_csv)

        i_cc += 50
        # print(df_out.shape)
        print()

    end_proc=time.time()
    print("Processing time:")
    print(end_proc - start_proc)
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year_string")
    parser.add_argument("i_cc_string")
    args = parser.parse_args()
    run_main(args.year_string, args.i_cc_string)
    