import pandas as pd
import time
from datetime import date
import math

def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/CIMS/"
    basepath_ftr = basepath+"python_pandas/CIMS/"
    basepath_csv = basepath+"csv/CIMS/"

    filename_core = "CIMSDATA_20230801_ext2" #"CIMSDATA_20231003_ext" # "CIMSDATA_20230801_ext" # 
    print("reading " + filename_core + " feather data")
    start = time.time()
    df_cims = pd.read_feather(basepath_ftr+filename_core + ".ftr")
    print(time.time() - start)
    print(df_cims.shape)

    print("Selecting only relevant columns...")
    use_cols = ["RINPERSOON","datetimeobj_prik","Vaccinnaam","Vaccinatiebatch","prik_nummer",
                "Toediener","Boostercode_oud","VaccinatieRangnummer","Vaccinatielabel"]
    df_cims = df_cims[use_cols]

    df_cims["keep"] = 0

    df_cims["covid_vax_firstdate"] = None
    df_cims["covid_vax_firstname"] = -1
    df_cims["covid_vax_firstbatch"] = -1
    df_cims["nr_covid_vax"] = 0

    df_cims["covid_vax_dates"] = None
    df_cims["covid_vax_name"] = None
    df_cims["covid_vax_batch"] = None
    df_cims["covid_vax_toediener"] = None
    df_cims["covid_vax_boostercode_oud"] = None
    df_cims["covid_vax_vaccinatierangnummer"] = None
    df_cims["covid_vax_vaccinatielabel"] = None

    print("processing...")

    start_overall = time.time()
    covid_vax_dates_list = []
    covid_vax_name_list = []
    covid_vax_batch_list = []
    covid_vax_toediener_list = []
    covid_vax_boostercode_oud_list = []
    covid_vax_vaccinatierangnummer_list = []
    covid_vax_vaccinatielabel_list = []
    prik_nummer = 0
    index_keep = 0

    rinp_str_prev = "NONE"
    start = time.time()
    for index, rowdata in df_cims.iterrows():
        if index % 100000 == 0:
            print(index)
            # print(rowdata)        
            print(time.time() - start)
            start = time.time()
            print()

        rinp_str = rowdata["RINPERSOON"]
        if rinp_str != rinp_str_prev:
            if rinp_str_prev != "NONE":
                covid_vax_dates_str = ';'.join(map(str,covid_vax_dates_list))
                df_cims.at[index_keep,"covid_vax_dates"]=covid_vax_dates_str
                covid_vax_name_str = ';'.join(map(str,covid_vax_name_list))
                df_cims.at[index_keep,"covid_vax_name"]=covid_vax_name_str
                covid_vax_batch_str = ';'.join(map(str,covid_vax_batch_list))
                df_cims.at[index_keep,"covid_vax_batch"]=covid_vax_batch_str
                covid_vax_toediener_str = ';'.join(map(str,covid_vax_toediener_list))
                df_cims.at[index_keep,"covid_vax_toediener"]=covid_vax_toediener_str
                covid_vax_boostercode_oud_str = ';'.join(map(str,covid_vax_boostercode_oud_list))
                df_cims.at[index_keep,"covid_vax_boostercode_oud"]=covid_vax_boostercode_oud_str
                covid_vax_vaccinatierangnummer_str = ';'.join(map(str,covid_vax_vaccinatierangnummer_list))
                df_cims.at[index_keep,"covid_vax_vaccinatierangnummer"]=covid_vax_vaccinatierangnummer_str
                covid_vax_vaccinatielabel_str = ';'.join(map(str,covid_vax_vaccinatielabel_list))
                df_cims.at[index_keep,"covid_vax_vaccinatielabel"]=covid_vax_vaccinatielabel_str
                df_cims.at[index_keep,"nr_covid_vax"]=prik_nummer
                                                         
            index_keep = index
            df_cims.at[index_keep,"keep"]=1
            covid_vax_dates_list = []
            covid_vax_name_list = []
            covid_vax_batch_list = []
            covid_vax_toediener_list = []
            covid_vax_boostercode_oud_list = []
            covid_vax_vaccinatierangnummer_list = []
            covid_vax_vaccinatielabel_list = []

            this_date = rowdata["datetimeobj_prik"]
            vaccinnaam = int(rowdata["Vaccinnaam"])
            vaccinatiebatch = int(rowdata["Vaccinatiebatch"])

            df_cims.at[index,"covid_vax_firstdate"]=this_date
            df_cims.at[index,"covid_vax_firstname"]=vaccinnaam
            df_cims.at[index,"covid_vax_firstbatch"]=vaccinatiebatch

            rinp_str_prev = rinp_str

        vaccinnaam = int(rowdata["Vaccinnaam"])
        vaccinatiebatch = int(rowdata["Vaccinatiebatch"])
        prik_nummer = int(rowdata["prik_nummer"])
        Toediener = int(rowdata["Toediener"])
        Boostercode_oud = int(rowdata["Boostercode_oud"])
        VaccinatieRangnummer = (rowdata["VaccinatieRangnummer"])
        if math.isnan(VaccinatieRangnummer):
            VaccinatieRangnummer = int(-1)
        else:
            VaccinatieRangnummer = int(VaccinatieRangnummer)
        Vaccinatielabel = int(rowdata["Vaccinatielabel"])

        this_date = rowdata["datetimeobj_prik"]
        covid_vax_dates_list.append(this_date)
        covid_vax_name_list.append(vaccinnaam)
        covid_vax_batch_list.append(vaccinatiebatch)

        covid_vax_toediener_list.append(Toediener)
        covid_vax_boostercode_oud_list.append(Boostercode_oud)
        covid_vax_vaccinatierangnummer_list.append(VaccinatieRangnummer)
        covid_vax_vaccinatielabel_list.append(Vaccinatielabel)

        # if index==1000:
        #     break
    
    # df_cims["datetimeobj_prik"] = datetimeobj_prik
    # df_cims["prik_nummer"] = prik_nummer

    print("Selecting only rows with data (keep)...")
    df_cims = df_cims[  df_cims['keep']==1 ]
    df_cims.reset_index(inplace=True,drop=True)
    print(df_cims.shape)

    print("Selecting only relevant columns...")
    use_cols = ["RINPERSOON","covid_vax_firstdate","covid_vax_firstname","covid_vax_firstbatch","nr_covid_vax",
                "covid_vax_dates","covid_vax_name","covid_vax_batch","covid_vax_toediener",
                "covid_vax_boostercode_oud", "covid_vax_vaccinatierangnummer", "covid_vax_vaccinatielabel"]
    df_cims = df_cims[use_cols]
    print(df_cims.shape)

    print("Overall processing time:")
    print(time.time() - start_overall)
    print()

    filename_core = "CIMSDATA_20230801_onerowpp"

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
    