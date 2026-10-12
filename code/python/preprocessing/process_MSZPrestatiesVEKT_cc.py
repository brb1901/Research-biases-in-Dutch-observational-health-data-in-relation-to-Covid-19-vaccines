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
    

def read_diagnosethesaurus():
    basepath = "H:/data/csv/diagnosethesaurus/" 
    filename_core = "20231011_090432_uitleverformaat4.3_AfleidingDBC"   
    print("reading " + filename_core + " csv data")
    # df_AflDBC = pd.read_csv(basepath + filename_core + ".csv")
    df_AflDBC = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)
    # df_AflDBC.fillna(-9999, inplace=True)
    # df_AflDBC.fillna("-9999", inplace=True)
    # df_AflDBC.loc[df_AflDBC["DBC_ID"].str.startswith('G', na=True), "DBC_ID"] = "-9999"
    # df_AflDBC.loc[df_AflDBC["DBC_ID"].str.startswith('Z', na=True), "DBC_ID"] = "-9999"
    # df_AflDBC.loc[df_AflDBC["DBC_ID"].str.startswith('M', na=True), "DBC_ID"] = "-9999"
    # print(ind)
    
    # "ConceptID","SpecialismeCode","DBC_ID"
    # df_AflDBC.ConceptID = df_AflDBC.ConceptID.astype(int)

    # df_AflDBC.SpecialismeCode = df_AflDBC.SpecialismeCode.astype(int)

    # df_AflDBC.DBC_ID = df_AflDBC.DBC_ID.astype(int)

    filename_core = "20231011_090432_uitleverformaat4.3_AfleidingICD10"   
    print("reading " + filename_core + " csv data")
    df_AflICD = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    filename_core = "20231011_090432_uitleverformaat4.3_BronICD10"   
    print("reading " + filename_core + " csv data")
    df_BronICD = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    filename_core = "20231011_090432_uitleverformaat4.3_BronSpecialisme"   
    print("reading " + filename_core + " csv data")
    df_BronSpec = pd.read_csv(basepath + filename_core + ".csv")

    return [df_AflDBC, df_AflICD, df_BronICD, df_BronSpec]


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


def parse_dbc_string(dbc):
    dbc_list = dbc.split('-')
    aaaa = (dbc_list[0])
    dddd = (dbc_list[3])
    return [aaaa, dddd]


def get_df_AflDBC_sel(df_AflDBC, aaaa,dddd):
    df_AflDBC_sel = df_AflDBC[ (df_AflDBC["SpecialismeCode"]==aaaa) & (df_AflDBC["DBC_ID"]==dddd) ] 
    return df_AflDBC_sel


def append_koppelIDPrestZa_zorgtype_list(rows, koppelIDPrestZa_list, zorgtype_list, j):
    koppelIDPrestZa_list.append(rows.iloc[j]["VEKTMSZKoppelIDPrestZa"])
    if rows.iloc[j]["VEKTMSZZorgtype"] != "99":
        zorgtype_list.append(rows.iloc[j]["VEKTMSZZorgtype"])
    return [koppelIDPrestZa_list, zorgtype_list]


def get_backup_df_AflDBC_sel(df_AflDBC, aaaa,dddd):
    df_AflDBC_sel = None
    try:                        
        dddd_int = int(dddd)
        dddd = str(dddd_int)
        # print("Trying different version")
        # print(dddd)
        df_AflDBC_sel = df_AflDBC[ (df_AflDBC["SpecialismeCode"]==aaaa) & (df_AflDBC["DBC_ID"]==dddd) ] 
        # print(df_AflDBC_sel)
    except:
        dddd_int = -9999
        # print("Trying different version failed.")
    return df_AflDBC_sel


def extend_ICD10_list(ICD10_list,df_AflICD,df_AflDBC_sel):
    df_AflICD_sel = df_AflICD[df_AflICD['ConceptID'].isin(df_AflDBC_sel['ConceptID'])]
    icd_list = df_AflICD_sel["ICD10"].tolist()
    # print(icd_list)
    ICD10_list.extend(icd_list)
    return ICD10_list


def make_list_strings(koppelIDPrestZa_list, zorgtype_list, ICD10_list):
    koppelIDPrestZa_str = ';'.join(map(str,koppelIDPrestZa_list))
    # print(koppelIDPrestZa_str)
    zorgtype_str = ';'.join(map(str,zorgtype_list))
    new_ICD_list = list(set(ICD10_list))
    # print(new_ICD_list)
    ICD10_str = ';'.join(map(str,new_ICD_list))
    # print(ICD10_str) 
    return [koppelIDPrestZa_str,zorgtype_str,ICD10_str]  


def process_person(rinp_str, df_in, df_AflDBC, df_AflICD, max_rinp_int_file_prev, file_ID, file_ID_new, year):
    rinp_int = int(rinp_str)
    if rinp_int <= max_rinp_int_file_prev:
        file_ID_this = file_ID
    else:
        file_ID_this = file_ID_new
    # print(rinp_str)
    df_pre = df_in[df_in["RINPERSOON"]==rinp_str]
    # print(rows.size)
    # print(len(rows))
    df_indiv = pd.DataFrame(columns=["RINPERSOON","year","quarter","file_ID_Prest","koppelIDPrestZa_list","nr_Prest",
                                        "ICD10_list","zorgtype_list"])
    for yq in [1,2,3,4]:
        # print(yq)
        date_from = get_date_from_quarter_excl(year, yq, False)
        date_to = get_date_from_quarter_excl(year, yq, True)
        rows = get_rows_df_fromdates(df_pre, date_from, date_to)
           
        koppelIDPrestZa_list = []
        ICD10_list = []
        #VEKTMSZZorgtype
        zorgtype_list = []
        nr_Prest = len(rows)
        for j in range(nr_Prest):
            [koppelIDPrestZa_list, zorgtype_list] = append_koppelIDPrestZa_zorgtype_list(rows, koppelIDPrestZa_list, zorgtype_list, j)

            dbc = rows.iloc[j]["VEKTMSZSpecialismeDiagnoseCombinatie"]
            if dbc != "9999-99-99-9999":
                # print(dbc)
                [aaaa, dddd] = parse_dbc_string(dbc)
                # print(aaaa)
                # print(dddd)
                df_AflDBC_sel = get_df_AflDBC_sel(df_AflDBC, aaaa,dddd)
                
                # print(df_AflDBC_sel)
                if len(df_AflDBC_sel)==0:
                    df_AflDBC_sel = get_backup_df_AflDBC_sel(df_AflDBC, aaaa,dddd)
                    try:                        
                        dddd_int = int(dddd)
                        dddd = str(dddd_int)
                        # print("Trying different version")
                        # print(dddd)
                        df_AflDBC_sel = df_AflDBC[ (df_AflDBC["SpecialismeCode"]==aaaa) & (df_AflDBC["DBC_ID"]==dddd) ] 
                        # print(df_AflDBC_sel)
                    except:
                        dddd_int = -9999
                        # print("Trying different version failed.")
                # icd_list = df_AflDBC_sel["ConceptID"]
                if df_AflDBC_sel is not None and len(df_AflDBC_sel):
                    ICD10_list = extend_ICD10_list(ICD10_list,df_AflICD,df_AflDBC_sel)
                    
            # print()
        [koppelIDPrestZa_str,zorgtype_str,ICD10_str] = make_list_strings(koppelIDPrestZa_list, zorgtype_list, ICD10_list)
        
        df_indiv.loc[yq-1] =  pd.Series({"RINPERSOON": rinp_str,
                                            "year": year,
                                            "quarter": yq,
                                            "file_ID_Prest": file_ID_this,
                                            "koppelIDPrestZa_list": koppelIDPrestZa_str,
                                            "nr_Prest": nr_Prest,
                                            "ICD10_list": ICD10_str,
                                            "zorgtype_list": zorgtype_str})
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

    [df_AflDBC, df_AflICD, df_BronICD, df_BronSpec] = read_diagnosethesaurus()
    # print(df_AflDBC)

    use_cols = ['RINPERSOON','datetimeobj_begin','RINP_int','VEKTMSZKoppelIDPrestZa','VEKTMSZZorgtype',
                'VEKTMSZSpecialismeDiagnoseCombinatie']

    year = int(year_string)
    # year = 2018
    # for year in [2018, 2019, 2020, 2021]:
    yearstr = str(year)
    print(year)
        # for i_cc in [0,50,100]:
    i_cc = int(i_cc_string) # 0
    special_case_end_file = False
    filename_core = "MSZPrestatiesVEKT" + yearstr + "_cc_" + str(i_cc) + ".ftr" # "_total.ftr" "_cc_
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

        filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
        filename_ftr = basepath_ftr + filename_core + ".ftr" 

        file_exists = os.path.exists(filename_ftr)
        if not file_exists:
            start_proc = time.time()    

            if special_case_end_file:
                print("special_case_end_file = True")
                # exit(1)
                i_cc += 50
                special_case_end_file = False
                filename_core = "MSZPrestatiesVEKT" + yearstr + "_cc_" + str(i_cc) + ".ftr" # "_total.ftr" "_cc_
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
                    # 

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
                df_indiv = process_person(rinp_str, df_in, df_AflDBC, df_AflICD, max_rinp_int_file_prev, file_ID, file_ID_new, year)
                
                # print(df_indiv)
                df_out = make_extend_df_out(df_indiv, df_out, i)            

            print(df_out.shape)
            # print(df_out)

            filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + yearstr + "_" + str(min_rinp_int) + "_" + str(max_rinp_int) +  versionstr
            filename_ftr = basepath_ftr + filename_core + ".ftr" 
            print("writing: "+filename_ftr)
            start = time.time()
            df_out.to_feather(filename_ftr)
            print(time.time() - start)
            filename_csv = basepath_csv + filename_core + "_head.csv"
            print("writing: "+filename_csv)
            df_out.head(100).to_csv(filename_csv)

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
    