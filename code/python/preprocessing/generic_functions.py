import pandas as pd
import pyreadstat
import time
import gc


def save_file(df, filename_core,path_ftr,path_dta,path_csv):
    print("Skipping csv now!")
    # filename_csv = path_csv+filename_core+"_head.csv"
    # print("writing (head): "+filename_csv)
    # start = time.time()
    # df.head(100).head().to_csv(filename_csv)
    # print(time.time() - start)

    filename_ftr = path_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df.to_feather(filename_ftr)
    print(time.time() - start)

    print("Skipping dta (Stata) now!")
    # filename_dta = path_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df.to_stata(filename_dta)
    # print(time.time() - start)


def convert_spss_chunks(path_sav,filename_core_sav,filename_core,path_ftr,path_dta,path_csv, usecols=None, chunksiz=10000):
    filename_sav = path_sav+filename_core_sav+".sav"

    start = time.time()
    reader = pyreadstat.read_file_in_chunks(pyreadstat.read_sav, filename_sav, chunksize = chunksiz)

    ind = 0
    for df, meta in reader:
        print(ind)
        # print(df.shape)
        if usecols is not None:
            print("selecting columns")
            # start = time.time()
            df2 = df[usecols]
            df.iloc[0:0]
            del df
            gc.collect()
            df = df2
            df2.iloc[0:0]
            del df2
            gc.collect()
            print(time.time() - start)
        
        # print(df.shape)
        # print(df)
        filename = filename_core + "_" + str(ind)
        save_file(df, filename,path_ftr,path_dta,path_csv)
        ind+=1
        # df.iloc[0:0]
        # del df
        # gc.collect()
        print()

    print("Total processing time of convert_spss_chunks:")
    print(time.time() - start)


def convert_spss(path_sav,filename_core_sav,filename_core,path_ftr,path_dta,path_csv, usecols=None):
    filename_sav = path_sav+filename_core_sav+".sav"
    print("reading: "+filename_sav)
    start = time.time()
    df, meta = pyreadstat.read_sav(filename_sav)
    print(time.time() - start)

    if usecols is not None:
        print("selecting columns")
        start = time.time()
        df2 = df[usecols]
        df.iloc[0:0]
        del df
        gc.collect()
        df = df2
        df2.iloc[0:0]
        del df2
        gc.collect()
        print(time.time() - start)

    filename_csv = path_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df.head(1000).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = path_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df.to_feather(filename_ftr)
    print(time.time() - start)

    print("Skipping dta (Stata) now!")
    # filename_dta = path_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df.to_stata(filename_dta)
    # print(time.time() - start)

    print("\n")
    df.iloc[0:0]
    del df
    gc.collect()

def convert_spsscsv(path_sav,filename_core_sav,filename_core,path_ftr,path_dta,path_csv, usecols=None):
    filename_sav = path_sav+filename_core_sav+".csv"
    print("reading: "+filename_sav)
    start = time.time()
    df = pd.read_csv(filename_sav)
    df, meta = pyreadstat.read_sav(filename_sav)
    print(time.time() - start)

    if usecols is not None:
        print("selecting columns")
        start = time.time()
        df2 = df[usecols]
        df.iloc[0:0]
        del df
        gc.collect()
        df = df2
        df2.iloc[0:0]
        del df2
        gc.collect()
        print(time.time() - start)

    filename_csv = path_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df.head().to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = path_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df.to_feather(filename_ftr)
    print(time.time() - start)

    # print("Skipping dta (Stata) now!")
    filename_dta = path_dta+filename_core+".dta"
    print("writing: "+filename_dta)
    start = time.time()
    df.to_stata(filename_dta)
    print(time.time() - start)

    print("\n")
    df.iloc[0:0]
    del df
    gc.collect()

