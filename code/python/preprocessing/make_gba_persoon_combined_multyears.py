import pandas as pd
import time
# from datetime import date

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


def process_data_oneyear(year, basepath_dta, basepath_ftr, basepath_csv):
    yearstr = str(year)
    print("reading GBAPERSOON" + yearstr + " feather data")
    start = time.time()
    df_p = pd.read_feather(basepath_ftr+"GBAPERSOON" + yearstr + ".ftr")
    print(time.time() - start)
    print(df_p.shape)

    print("computing and adding leeftijd_in_ditjaar")
    start = time.time()
    # l_in_ditjaar = -1
    # leeftijd_in_ditjaar = []
    # for index, rowdata in df_p.iterrows():
    #     if index % 100000 == 0:
    #         print(index)
    #         print(l_in_ditjaar)
    #     yearborn = int(rowdata["GBAGEBOORTEJAAR"])
    #     l_in_ditjaar = year - yearborn
    #     leeftijd_in_ditjaar.append(l_in_ditjaar)
    # df_p["leeftijd_in_ditjaar"] = leeftijd_in_ditjaar
    df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    df_p["leeftijd_in_ditjaar"] = year - df_p["GBAGEBOORTEJAAR"]
    print(time.time() - start)

    filename_core = "GBAPERSOON" + yearstr + "_ext"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_p.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_p.to_feather(filename_ftr)
    print(time.time() - start)

    print("Skipping dta (Stata) now!")
    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_p.to_stata(filename_dta)
    # print(time.time() - start)


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    yearfirst = 2015

    for year in [2015, 2016, 2017, 2018, 2019, 2020, 2021]: # 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
        yearstr = str(year)
        if year == yearfirst:            
            print("reading GBAPERSOON" + yearstr + " feather data")
            # start = time.time()
            df_p1 = pd.read_feather(basepath_ftr+"GBAPERSOON" + yearstr + ".ftr")
            # print(time.time() - start)            
        else:
            print("Using merged pd from year " + yearstr)
            df_p1 = df_p
        print(df_p1.shape)

        yearnext = year + 1
        yearnextstr = str(yearnext)
        print("reading GBAPERSOON" + yearnextstr + " feather data")
        # start = time.time()
        df_p2 = pd.read_feather(basepath_ftr+"GBAPERSOON" + yearnextstr + ".ftr")
        # print(time.time() - start)
        print(df_p2.shape)

        # df_ptotal = pd.merge(df_p1, df_p2, how='outer', on=['RINPERSOON'])
        print("Merging")
        df_p = pd.concat([df_p1, df_p2])
        print("Dropping duplicates")
        df_p.drop_duplicates(inplace=True, keep='last')
        df_p.reset_index(inplace=True,drop=True)


    print(df_p.shape)
    df_p["GBAGEBOORTEJAAR"]=  df_p["GBAGEBOORTEJAAR"].astype('int')
    # df_p.reset_index(inplace=True,drop=True)

    filename_core = "GBAPERSOON_combined_years2015-2022_ext"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_p.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_p.to_feather(filename_ftr)
    print(time.time() - start)

    print("Skipping dta (Stata) now!")
    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_p.to_stata(filename_dta)
    # print(time.time() - start)

if __name__ == '__main__':
    run_main()


    