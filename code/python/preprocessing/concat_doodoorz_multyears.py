import pandas as pd
import time

def run_main():
    basepath = "H:/data/"

    year = 2020 # 2019 # 2018 2021 # 
    year_tostop = 2024 # 2022 # 
    # 
    yearsstr =   "2020-2023" # "2021" # "2013-2023"
    # year_prev = year - 1
    nr_files = 0
    while year<year_tostop: # and weeknr <=6:       
        yearstr = str(year)
        print(year)
        filename_core = "DOODOORZ" + yearstr 
        print("reading " + filename_core + " feather data")
        df_do = pd.read_feather(basepath+"python_pandas/DOODOORZ/" + filename_core + ".ftr")
        print(df_do.shape)
        if nr_files == 0:
            df_total = df_do
        else:
            df_total = df_total.append(df_do)
        nr_files += 1
        print(df_total.shape)
        year += 1
    
    df_total.reset_index(inplace=True,drop=True)

    filename_core = "DOODOORZ" + yearsstr
    filename_csv = basepath+"csv/DOODOORZ/"+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_total.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath+"python_pandas/DOODOORZ/"+filename_core+".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_total.to_feather(filename_ftr)
    print(time.time() - start)



if __name__ == '__main__':
    run_main()
