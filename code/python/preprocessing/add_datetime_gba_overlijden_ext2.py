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

    print("reading GBAOVERLIJDEN2023_ext feather data")
    start = time.time()
    df_overlijden = pd.read_feather(basepath_ftr+"GBAOVERLIJDEN2023_ext.ftr")
    print(time.time() - start)
    print(df_overlijden.shape)

    size = len(df_overlijden["RINPERSOON"])
    print(size)
    datetimeobj_overlijden = [None] * size
    age = -1
    rowdata = 0
    row = 0
    start = time.time()
    for index, rowdata in df_overlijden.iterrows():
        if index % 100000 == 0:
            print(index)
            print(age)
            print(rowdata)
            print(row)            
            print(time.time() - start)
            start = time.time()
            print()
        
        date_of_interest = date(rowdata["jaar_overlijden"],rowdata["maand_overlijden"],rowdata["dag_overlijden"])            
        # datetimeobj_overlijden.append(date_of_interest)
        datetimeobj_overlijden[index] = date_of_interest
            
        # if index==1000:
        #     break


    df_overlijden["datetimeobj_overlijden"] = datetimeobj_overlijden

    filename_core = "GBAOVERLIJDEN2023_ext2"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_overlijden.head(200).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_overlijden.to_feather(filename_ftr)
    print(time.time() - start)

    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_overlijden.to_stata(filename_dta)
    # print(time.time() - start)
    

        