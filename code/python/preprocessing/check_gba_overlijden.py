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
    # start = time.time()
    df_persoon = pd.read_feather(basepath_ftr+"GBAPERSOON_combined_years2015-2022_ext.ftr") # GBAPERSOON2018
    # print(time.time() - start)

    print("reading GBAOVERLIJDEN2022 feather data")
    # start = time.time()
    df_overlijden = pd.read_feather(basepath_ftr+"GBAOVERLIJDEN2022.ftr")
    # print(time.time() - start)
    print(df_overlijden.shape)

    rowdata = 0
    row = 0
    jaar_overlijden = []
    for index, rowdata in df_overlijden.iterrows():
        if index % 100000 == 0:
            print(index)
            print(rowdata)
            print(row)            
            print()        
        age = -1
        overlstr = rowdata["GBADatumOverlijden"]
        y = int(overlstr[0:4])        
        jaar_overlijden.append(y)

    df_overlijden["jaar_overlijden"] = jaar_overlijden

    df_overlijden = df_overlijden[ (df_overlijden['jaar_overlijden']>=2015)  ] 
    print(df_overlijden.shape)

    print("\nmerging\n")
    start = time.time()
    df_overlijden_ext = pd.merge(df_persoon, df_overlijden, how='inner', on=['RINPERSOON'])
    print(time.time() - start)
    print(df_overlijden.shape)

    
    

        