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


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/CIMS/"
    basepath_ftr = basepath+"python_pandas/CIMS/"
    basepath_csv = basepath+"csv/CIMS/"

    print("reading GBAPERSOON2020 feather data")
    start = time.time()
    df_persoon = pd.read_feather("H:/data/python_pandas/GBA/GBAPERSOON2020_presentinyear_incldead.ftr")
    print(time.time() - start)

    filename_core = "CIMSDATA_20230801" # "CIMSDATA_20231120" # "CIMSDATA_20231003" # "CIMSDATA_20230801" #
    print("reading " + filename_core + " feather data")
    start = time.time()
    df_cims = pd.read_feather(basepath_ftr+ filename_core + ".ftr")
    print(time.time() - start)
    df_cims.rename(columns={'Rinpersoon': 'RINPERSOON'}, inplace=True)
    print(df_cims)

    print("\nmerging\n")
    start = time.time()
    df_cims_ext = pd.merge(df_cims, df_persoon, how='inner', on=['RINPERSOON'], validate='many_to_one')
    print(time.time() - start)
    print(df_cims_ext)

    leeftijd_prik = []
    jaar_prik = []
    maand_prik = []
    dag_prik = []
    jaar_geb = []
    maand_geb = []
    age = -1
    rowdata = 0
    row = 0
    start = time.time()
    for index, rowdata in df_cims_ext.iterrows():
        if index % 100000 == 0:
            print(index)
            print(age)
            print(rowdata)
            print(row)            
            print(time.time() - start)
            start = time.time()
            print()
        
        age = -1
        prikdatstr = rowdata["Vaccinatiedatum"]
        y = int(prikdatstr[0:4])
        # Alleen mensen vanaf 2017 (overleden) checken
        # if y>=2017:
        # rinp = rowdata["RINPERSOON"]
        # row = df_persoon.loc[df_persoon["RINPERSOON"]==rinp]
        # if row.size: 
        # We weten niet de geboorteDAG, dus kiezen we midden van maand (15)
        geb_jaar = int(rowdata["GBAGEBOORTEJAAR"])
        geb_maand = int(rowdata["GBAGEBOORTEMAAND"])
        date_born = date(geb_jaar,geb_maand,15)
        # y_born = int(row.iloc[0]["GBAGEBOORTEJAAR"])
        
        # age = y-y_born
        m = int(prikdatstr[4:6])
        d = int(prikdatstr[6:8])
        date_of_interest = date(y,m,d)
        age = calculate_age(date_born, date_of_interest)
            
        leeftijd_prik.append(age)
        jaar_prik.append(y)
        maand_prik.append(m)
        dag_prik.append(d)
        jaar_geb.append(geb_jaar)
        maand_geb.append(geb_maand)

    use_cols = ['RINPERSOON','Vaccinatiedatum','Vaccinnaam','Vaccinatiebatch','Toediener','Boostercode_oud','VaccinatieRangnummer','Vaccinatielabel',
            'GBAGESLACHT']
    df_cims_ext = df_cims_ext[use_cols]
    
    df_cims_ext["leeftijd_prik"] = leeftijd_prik
    df_cims_ext["jaar_prik"] = jaar_prik
    df_cims_ext["maand_prik"] = maand_prik
    df_cims_ext["dag_prik"] = dag_prik
    df_cims_ext["jaar_geb"] = jaar_geb
    df_cims_ext["maand_geb"] = maand_geb

    filename_core += "_ext"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_cims_ext.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_cims_ext.to_feather(filename_ftr)
    print(time.time() - start)

    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_cims_ext.to_stata(filename_dta)
    # print(time.time() - start)
    

if __name__ == '__main__':
    run_main()
    