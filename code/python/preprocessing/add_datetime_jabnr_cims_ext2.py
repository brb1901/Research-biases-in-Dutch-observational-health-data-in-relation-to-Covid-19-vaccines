import pandas as pd
import time
from datetime import date


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/CIMS/"
    basepath_ftr = basepath+"python_pandas/CIMS/"
    basepath_csv = basepath+"csv/CIMS/"

    filename_core = "CIMSDATA_20231120_ext" #"CIMSDATA_20231003_ext" # "CIMSDATA_20230801_ext" # 
    print("reading " + filename_core + " feather data")
    start = time.time()
    df_cims = pd.read_feather(basepath_ftr+filename_core + ".ftr")
    print(time.time() - start)
    print(df_cims.shape)

    size = len(df_cims["RINPERSOON"])
    print(size)
    datetimeobj_prik = [None] * size
    prik_nummer = [int(0)] * size
    # datetimeobj_prik = []
    # prik_nummer = []
    rowdata = 0
    row = 0
    rinp = -99
    rinp_prev = -99
    priknr = 1
    start = time.time()
    for index, rowdata in df_cims.iterrows():
        if index % 100000 == 0:
            print(index)
            print(rowdata)
            print(row)            
            print(time.time() - start)
            start = time.time()
            print()

        date_of_interest = date(rowdata["jaar_prik"],rowdata["maand_prik"],rowdata["dag_prik"])            
        # datetimeobj_prik.append(date_of_interest)
        datetimeobj_prik[index] = date_of_interest
        
        rinp = rowdata["RINPERSOON"]
        if rinp != rinp_prev:
            priknr = 1
        else:
            if index>0:
                # priknr_prev = prik_nummer[-1]
                priknr_prev = prik_nummer[index-1]
            else:
                priknr_prev = 0
            priknr = priknr_prev+1
        # prik_nummer.append(priknr)
        prik_nummer[index] = int(priknr)
        rinp_prev = rinp

        # if index==1000:
        #     break
    
    df_cims["datetimeobj_prik"] = datetimeobj_prik
    df_cims["prik_nummer"] = prik_nummer

    filename_core += "2"

    filename_csv = basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_cims.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_cims.to_feather(filename_ftr)
    print(time.time() - start)

    # # ZONDER datetimeobj_prik!! (want dit type niet ondersteund voor dta/stata; geen info verloren want 
    # # complete datum verder aanwezig)
    # use_cols = ['RINPERSOON','Vaccinatiedatum','Vaccinnaam','Vaccinatiebatch','Toediener','Boostercode_oud','VaccinatieRangnummer','Vaccinatielabel',
    #         'GBAGESLACHT','leeftijd_prik','jaar_prik','maand_prik','dag_prik', 'prik_nummer']
    # df_cims = df_cims[use_cols]
    
    #DEBUG werkt niet!!??
    # filename_dta = basepath_dta+filename_core+".dta"
    # print("writing: "+filename_dta)
    # start = time.time()
    # df_cims.to_stata(filename_dta)
    # print(time.time() - start)
    

if __name__ == '__main__':
    run_main()
    