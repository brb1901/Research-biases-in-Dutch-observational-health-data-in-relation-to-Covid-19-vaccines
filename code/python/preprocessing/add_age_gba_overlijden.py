import pandas as pd
import time
from datetime import date

def calculate_age(date_born, date_of_interest):
    try:
        birthday = date_born.replace(year = date_of_interest.year)

    # raised when birth date is Feb 29
    # and year is not leap year
    except ValueError:
        birthday = date_born.replace(year = date_of_interest.year,
                month = date_born.month, day = 1)
    
    if birthday > date_of_interest:
        return date_of_interest.year - date_born.year - 1
    else:
        return date_of_interest.year - date_born.year


if __name__ == '__main__':
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    print("reading GBAPERSOON_combined_years2015-2022_ext feather data")
    start = time.time()
    df_persoon = pd.read_feather(basepath_ftr+"GBAPERSOON_combined_years2015-2022_ext.ftr") # GBAPERSOON2018
    print(time.time() - start)

    print("reading GBAOVERLIJDEN2023 feather data")
    start = time.time()
    df_overlijden = pd.read_feather(basepath_ftr+"GBAOVERLIJDEN2023.ftr")
    print(time.time() - start)
    print(df_overlijden)

    print("\nmerging\n")
    start = time.time()
    df_overlijden_ext = pd.merge(df_persoon, df_overlijden, how='inner', on=['RINPERSOON'])
    print(time.time() - start)
    print(df_overlijden_ext)

    leeftijd_overlijden = []
    jaar_overlijden = []
    maand_overlijden = []
    dag_overlijden = []
    age = -1
    rowdata = 0
    row = 0
    start = time.time()
    for index, rowdata in df_overlijden_ext.iterrows():
        if index % 100000 == 0:
            print(index)
            print(age)
            print(rowdata)
            print(row)            
            print(time.time() - start)
            start = time.time()
            print()
        
        age = -1
        overlstr = rowdata["GBADatumOverlijden"]
        y = int(overlstr[0:4])
        # Alleen mensen vanaf 2017 (overleden) checken
        # if y>=2017:
        # rinp = rowdata["RINPERSOON"]
        # row = df_persoon.loc[df_persoon["RINPERSOON"]==rinp]
        # if row.size: 
        # We weten niet de geboorteDAG, dus kiezen we midden van maand (15)
        date_born = date(int(rowdata["GBAGEBOORTEJAAR"]),int(rowdata["GBAGEBOORTEMAAND"]),15)
        # y_born = int(row.iloc[0]["GBAGEBOORTEJAAR"])
        
        # age = y-y_born
        m = int(overlstr[4:6])
        d = int(overlstr[6:8])
        date_of_interest = date(y,m,d)
        age = calculate_age(date_born, date_of_interest)
            
        leeftijd_overlijden.append(age)
        jaar_overlijden.append(y)
        maand_overlijden.append(m)
        dag_overlijden.append(d)

    use_cols = ['RINPERSOON','GBADatumOverlijden','GBAGESLACHT',"GBAGEBOORTEJAAR"]
    df_overlijden_ext = df_overlijden_ext[use_cols]
    
    df_overlijden_ext["leeftijd_overlijden"] = leeftijd_overlijden
    df_overlijden_ext["jaar_overlijden"] = jaar_overlijden
    df_overlijden_ext["maand_overlijden"] = maand_overlijden
    df_overlijden_ext["dag_overlijden"] = dag_overlijden

    filename_core = "GBAOVERLIJDEN2023_ext"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_overlijden_ext.head(200).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_overlijden_ext.to_feather(filename_ftr)
    print(time.time() - start)

    filename_dta = basepath_dta+filename_core+".dta"
    print("writing: "+filename_dta)
    start = time.time()
    df_overlijden_ext.to_stata(filename_dta)
    print(time.time() - start)
    

        