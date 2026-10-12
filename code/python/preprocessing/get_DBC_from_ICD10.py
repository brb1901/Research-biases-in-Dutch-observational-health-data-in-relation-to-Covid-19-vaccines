import os
import pandas as pd
import time
import argparse
from datetime import date, datetime, timedelta
import gc


def read_diagnosethesaurus():
    basepath = "H:/data/csv/diagnosethesaurus/" 
    filename_core = "20231011_090432_uitleverformaat4.3_AfleidingDBC"   
    print("reading " + filename_core + " csv data")
    df_AflDBC = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    filename_core = "20231011_090432_uitleverformaat4.3_AfleidingICD10"   
    print("reading " + filename_core + " csv data")
    df_AflICD = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    filename_core = "20231011_090432_uitleverformaat4.3_BronICD10"   
    print("reading " + filename_core + " csv data")
    df_BronICD = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    filename_core = "20231011_090432_uitleverformaat4.3_BronSpecialisme"   
    print("reading " + filename_core + " csv data")
    df_BronSpec = pd.read_csv(basepath + filename_core + ".csv")

    filename_core = "20231011_090432_uitleverformaat4.3_BronDBC"   
    print("reading " + filename_core + " csv data")
    df_BronDBC = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    return [df_AflDBC, df_AflICD, df_BronICD, df_BronSpec, df_BronDBC]

def read_verrichtingenthesaurus():
    basepath = "H:/data/csv/diagnosethesaurus/" 
    filename_core = "20231016_095421_uitleverformaat4.3_VT_BronZA"   
    print("reading " + filename_core + " csv data")
    df_BronZA = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)

    print("making dict")
    dict_BronZA = dict(zip(df_BronZA.ZA_Code,df_BronZA.ZPK_code))

    return [df_BronZA, dict_BronZA]



def parse_dbc_string(dbc):
    dbc_list = dbc.split('-')
    aaaa = (dbc_list[0])
    dddd = (dbc_list[3])
    return [aaaa, dddd]


def get_df_AflDBC_sel(df_AflDBC, aaaa,dddd):
    df_AflDBC_sel = df_AflDBC[ (df_AflDBC["SpecialismeCode"]==aaaa) & (df_AflDBC["DBC_ID"]==dddd) ] 
    return df_AflDBC_sel



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




def run_main(icd10_str):
    # basepath = "H:/data/"

    [df_AflDBC, df_AflICD, df_BronICD, df_BronSpec, df_BronDBC] = read_diagnosethesaurus()
    [df_BronZA, dict_BronZA] = read_verrichtingenthesaurus()

    print()

    # [aaaa, dddd] = parse_dbc_string(dbc)
    # # print(aaaa)
    # # print(dddd)
    # df_AflDBC_sel = get_df_AflDBC_sel(df_AflDBC, aaaa,dddd)

    # df_AflDBC_sel = get_df_AflDBC_sel(df_AflDBC, aaaa,dddd)
    # df_AflDBC_sel = df_AflDBC[ (df_AflDBC["SpecialismeCode"]==aaaa) & (df_AflDBC["DBC_ID"]==dddd) ]
    df_AflICD_sel = df_AflICD[ (df_AflICD["ICD10"]==icd10_str) ]  
    if len(df_AflICD_sel)!=0:
        # df_AflICD_sel = df_AflICD[df_AflICD['ConceptID'].isin(df_AflDBC_sel['ConceptID'])]
        df_AflDBC_sel = df_AflDBC[df_AflDBC['ConceptID'].isin(df_AflICD_sel['ConceptID'])]
        SpecialismeCode_list = df_AflDBC_sel["SpecialismeCode"].tolist()
        DBC_ID_list = df_AflDBC_sel["DBC_ID"].tolist()

        i=0
        for SpecialismeCode in SpecialismeCode_list:
            aaaa = SpecialismeCode
            dddd = DBC_ID_list[i]
            df_BronDBC_sel = df_BronDBC[ (df_BronDBC["Specialismecode"]==aaaa) & (df_BronDBC["DBC_ID"]==dddd) ] 
            if len(df_BronDBC_sel)==0 and len(dddd):
                # df_AflDBC_sel = get_backup_df_AflDBC_sel(df_AflDBC, aaaa,dddd)                    
                dddd_int = int(dddd)
                dddd = str(dddd_int)
                # print("Trying different version")
                # print(dddd)
                df_BronDBC_sel = df_BronDBC[ (df_BronDBC["Specialismecode"]==aaaa) & (df_BronDBC["DBC_ID"]==dddd) ] 
            if df_BronDBC_sel is not None and len(df_BronDBC_sel):
                DBC_omschrijving = df_BronDBC_sel["DBC_omschrijving"].to_string() #.astype(str)
            else:
                DBC_omschrijving = "unknown"
                    
            print(SpecialismeCode + " - " + dddd + " - " + DBC_omschrijving ) #
            # print()
            i+=1
    
    # # print(df_AflDBC_sel)
    # if len(df_AflDBC_sel)==0:
    #     df_AflDBC_sel = get_backup_df_AflDBC_sel(df_AflDBC, aaaa,dddd)
    #     try:                        
    #         dddd_int = int(dddd)
    #         dddd = str(dddd_int)
    #         # print("Trying different version")
    #         # print(dddd)
    #         df_AflDBC_sel = df_AflDBC[ (df_AflDBC["SpecialismeCode"]==aaaa) & (df_AflDBC["DBC_ID"]==dddd) ] 
    #         # print(df_AflDBC_sel)
    #     except:
    #         dddd_int = -9999
    #         # print("Trying different version failed.")
    # # icd_list = df_AflDBC_sel["ConceptID"]
    # if df_AflDBC_sel is not None and len(df_AflDBC_sel):
    #     df_AflICD_sel = df_AflICD[df_AflICD['ConceptID'].isin(df_AflDBC_sel['ConceptID'])]
    #     icd_list = df_AflICD_sel["ICD10"].tolist()
    #     print(icd_list)
    # else:
    #     print("No match found.")
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("icd10_str")
    args = parser.parse_args()
    run_main(args.icd10_str)
    