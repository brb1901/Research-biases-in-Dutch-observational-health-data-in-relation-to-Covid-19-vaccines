import os
import pandas as pd
import time
from datetime import date, datetime
import argparse
import gc

def get_date_from_quarter(year, yq, to_bool=True):
    match yq:
        case 1:
            if to_bool:
                dt = datetime(year,3,31,23,59,59)
            else:
                dt = datetime(year,1,1,0,0,0)
        case 2:
            if to_bool:
                dt = datetime(year,6,30,23,59,59)
            else:
                dt = datetime(year,4,1,0,0,0)
        case 3:
            if to_bool:
                dt = datetime(year,9,30,23,59,59)
            else:
                dt = datetime(year,7,1,0,0,0)
        case 4:
            if to_bool:
                dt = datetime(year,12,31,23,59,59)
            else:
                dt = datetime(year,10,1,0,0,0)
        case _:
            dt = None
    return dt

def get_date_from_quarter_excl(year, yq, to_bool=True):
    match yq:
        case 1:
            if to_bool:
                dt = datetime(year,4,1,0,0,0)
            else:
                dt = datetime(year,1,1,0,0,0)
        case 2:
            if to_bool:
                dt = datetime(year,7,1,0,0,0)
            else:
                dt = datetime(year,4,1,0,0,0)
        case 3:
            if to_bool:
                dt = datetime(year,10,1,0,0,0)
            else:
                dt = datetime(year,7,1,0,0,0)
        case 4:
            if to_bool:
                dt = datetime(year+1,1,1,0,0,0)
            else:
                dt = datetime(year,10,1,0,0,0)
        case _:
            dt = None
    return dt

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
    

def read_verrichtingenthesaurus():
    basepath = "H:/data/csv/diagnosethesaurus/" 
    filename_core = "20231016_095421_uitleverformaat4.3_VT_BronZA"   
    print("reading " + filename_core + " csv data")
    # df_AflDBC = pd.read_csv(basepath + filename_core + ".csv")
    df_BronZA = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    print("making dict")
    dict_BronZA = dict(zip(df_BronZA.ZA_Code,df_BronZA.ZPK_code))

    return [df_BronZA, dict_BronZA]


def read_make_compact_df_pres(filename, use_cols):
    print("reading " + filename)
    start = time.time()    
    df_pres = pd.read_feather(filename)
    print(time.time() - start)
    # print(df_pres.shape)
    df_pres["RINP_int"] = df_pres["RINPERSOON"].astype(int)
    df_pres["datetimeobj_begin"] = pd.to_datetime(df_pres["VEKTMSZZorgactiviteitdatum"], errors='coerce')
    df_pres = select_cols(df_pres, use_cols)
    return df_pres


def check_meta_file(df_meta, filename_meta, filename):
    basepath = "H:/data/"
    filename_meta_csv = basepath +"csv/meta/files_meta.csv"
    file_meta_change = False
    row = df_meta.loc[df_meta["filename"]==filename]
    if row.size:
        file_ID = row.iloc[0]["file_ID"]
        print("file_ID found:")
    else:
        file_ID = len(df_meta)
        df_meta.loc[file_ID] =  pd.Series({"file_ID": file_ID, "filename": filename})
        file_meta_change = True

    if file_meta_change:
        print("new file_ID:")
        df_meta.to_feather(filename_meta)
        df_meta.to_csv(filename_meta_csv)
    print(file_ID)
    return file_ID


def get_rows_df_fromdates(df_pre, date_from, date_to):
    rows = df_pre.loc[ (df_pre["datetimeobj_begin"]>=date_from) & (df_pre["datetimeobj_begin"]<date_to) ]
    return rows


def make_list_strings(zorgactiviteit_list, zorgtypecode_list):
    zorgactiviteit_str = ';'.join(map(str,zorgactiviteit_list))
    # print(koppelIDPrestZa_str)
    zorgtypecode_str = ';'.join(map(str,zorgtypecode_list))
    # new_ICD_list = list(set(ICD10_list))
    # # print(new_ICD_list)
    # ICD10_str = ';'.join(map(str,new_ICD_list))
    # print(ICD10_str) 
    return [zorgactiviteit_str, zorgtypecode_str] 


def process_person(rinp_str, df_in, dict_BronZA, max_rinp_int_file_prev, file_ID, file_ID_new, year):
    rinp_int = int(rinp_str)
    if rinp_int <= max_rinp_int_file_prev:
        file_ID_this = file_ID
    else:
        file_ID_this = file_ID_new
    # print(rinp_str)
    df_pre = df_in[df_in["RINPERSOON"]==rinp_str]
    df_indiv = pd.DataFrame(columns=["RINPERSOON","year","quarter","file_ID_ZorgAct","nr_Act",
                                        "zorgactiviteit_list","zorgtypecode_list"])
    for yq in [1,2,3,4]:
        # print(yq)
        date_from = get_date_from_quarter_excl(year, yq, False)
        date_to = get_date_from_quarter_excl(year, yq, True)
        rows = get_rows_df_fromdates(df_pre, date_from, date_to)
        # print(rows.size)
        # print(len(rows))
           
        zorgactiviteit_list = []
        zorgtypecode_list = []
        nr_Act = len(rows)
        for j in range(nr_Act):
            # print(rows.iloc[j]["VEKTMSZZorgactiviteit"])
            zorgact = rows.iloc[j]["VEKTMSZZorgactiviteit"]
            if zorgact != "999999":
                zorgactiviteit_list.append(zorgact)
                # print(zorgact)
                zorgcode = dict_BronZA[zorgact]
                # print(zorgcode)
                zorgtypecode_list.append(str(zorgcode))

        [zorgactiviteit_str, zorgtypecode_str] = make_list_strings(zorgactiviteit_list, zorgtypecode_list)
        # print(zorgtypecode_str)
        
        df_indiv.loc[yq-1] =  pd.Series({"RINPERSOON": rinp_str,
                                            "year": year,
                                            "quarter": yq,
                                            "file_ID_ZorgAct": file_ID_this,
                                            "nr_Act": nr_Act,
                                            "zorgactiviteit_list": zorgactiviteit_str,
                                            "zorgtypecode_list": zorgtypecode_str})
        
    # exit(1)
    return df_indiv


def make_extend_df_out(df_indiv, df_out, i):
    if i==0:
        df_out = df_indiv
    else:
        df_out = pd.concat([df_out,df_indiv], ignore_index=True)
        # df_out.append(df_indiv)
        df_out.reset_index(inplace=True,drop=True)
    return df_out


def run_main(year_string, i_cc_string):
    basepath = "H:/data/"
    basepath_ftr = basepath +"python_pandas/VEKTIS/"
    basepath_csv = basepath +"csv/VEKTIS/"

    versionstr = "_v0"

    [df_BronZA, dict_BronZA] = read_verrichtingenthesaurus()
    # zorgact = "039757"
    # print(zorgact)
    # zorgcode = dict_BronZA[zorgact]
    # print(zorgcode)

    # print(df_AflDBC)

    use_cols = ['RINPERSOON','datetimeobj_begin','RINP_int','VEKTMSZZorgactiviteitdatum','VEKTMSZZorgactiviteit']

    year = int(year_string)
    # year = 2018
    # for year in [2018, 2019, 2020, 2021]:
    yearstr = str(year)
    print(year)
        # for i_cc in [0,10,20]:
    i_cc = int(i_cc_string) # 0
    special_case_end_file = False
    filename_core = "MSZZorgactiviteitenVEKT" + yearstr + "_cc_" + str(i_cc) + ".ftr" # "_total.ftr" "_cc_
    filename = basepath_ftr + filename_core

    filename_meta = basepath +"python_pandas/meta/files_meta.ftr"
    file_exists_meta = os.path.exists(filename_meta)
    if file_exists_meta:
        print("reading " + filename_meta)
        df_meta = pd.read_feather(filename_meta)        
    else:
        print("making " + filename_meta)
        df_meta = pd.DataFrame(columns=["file_ID","filename"])
    file_ID = check_meta_file(df_meta, filename_meta, filename)
    file_ID_new = file_ID
        
    df_pres = read_make_compact_df_pres(filename, use_cols)

    max_rinp_int_file = df_pres["RINP_int"].max()
    print("max_rinp_int_file")
    print(max_rinp_int_file)
    max_rinp_int_file_prev = max_rinp_int_file

    # min_rinp_int_file = df_pres["RINP_int"].min()

    max_rinp_int = 0
    min_rinp_int = 1
    final_batch = False
    while (min_rinp_int < max_rinp_int_file) and ~final_batch:
        min_rinp_int = max_rinp_int+1
        max_rinp_int = min_rinp_int-1 + 1000000 # 1000 #
        if max_rinp_int > max_rinp_int_file:
            special_case_end_file = True
        print(min_rinp_int)
        print(max_rinp_int)

        filename_core =  "VEKTIS_ZorgActPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
        filename_ftr = basepath_ftr + filename_core + ".ftr" 

        file_exists = os.path.exists(filename_ftr)
        if not file_exists:
            start_proc = time.time()    

            if special_case_end_file:
                print("special_case_end_file = True")
                # exit(1)
                i_cc += 10
                special_case_end_file = False
                filename_core = "MSZZorgactiviteitenVEKT" + yearstr + "_cc_" + str(i_cc) + ".ftr" # "_total.ftr" "_cc_
                print("trying:")
                print(filename_core)
                filename = basepath_ftr + filename_core
                if os.path.exists(filename):
                    file_ID_new = check_meta_file(df_meta, filename_meta, filename)
                    df_pres = df_pres[ (df_pres["RINP_int"] >= min_rinp_int)  ]
                    df_pres_new = read_make_compact_df_pres(filename, use_cols)
                    df_pres = pd.concat([df_pres,df_pres_new], ignore_index=True)
                    df_pres.reset_index(inplace=True,drop=True)
                    df_pres_new.iloc[0:0]
                    del df_pres_new
                    gc.collect()
                    max_rinp_int_file_prev = max_rinp_int_file
                    max_rinp_int_file = df_pres["RINP_int"].max()
                    print("new max_rinp_int_file")
                    print(max_rinp_int_file)
                else:
                    if final_batch:
                        print("Done!")
                        exit(1)
                    else:
                        print("No more files. Final batch.")
                        final_batch = True
                     

            df_in = df_pres[ (df_pres["RINP_int"] >= min_rinp_int) & (df_pres["RINP_int"] <= max_rinp_int) ]

            rinp_ser = df_in["RINPERSOON"].unique()
            nr_rinp = len(rinp_ser)
            print("Number of people in this batch:")
            print(nr_rinp)
            df_out = None
            for i in range(nr_rinp): # range(10): #range(nr_rinp):
                if i % 1000 == 0:
                    print(i)
                    # if i == 5000:
                    #     exit(1)
                rinp_str = rinp_ser[i]
                df_indiv = process_person(rinp_str, df_in, dict_BronZA, max_rinp_int_file_prev, file_ID, file_ID_new, year)
                
                # print(df_indiv)
                df_out = make_extend_df_out(df_indiv, df_out, i)      

                # #DEBUG ***
                # exit(1)      

            
            
            if df_out is not None:
                print(df_out.shape)
                # print(df_out)

                filename_core =  "VEKTIS_ZorgActPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
                filename_ftr = basepath_ftr + filename_core + ".ftr" 
                print("writing: "+filename_ftr)
                start = time.time()
                df_out.to_feather(filename_ftr)
                print(time.time() - start)
                filename_csv = basepath_csv + filename_core + "_head.csv"
                print("writing: "+filename_csv)
                df_out.head(100).to_csv(filename_csv)
            else:
                print("Empty df_out!")

            end_proc=time.time()
            print("Processing time:")
            print(end_proc - start_proc)
            # #DEBUG ***
            # exit(1)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year_string")
    parser.add_argument("i_cc_string")
    args = parser.parse_args()
    run_main(args.year_string, args.i_cc_string)
    