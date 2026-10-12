import os
import pandas as pd
import time

def run_main():
    basepath = "T:/" # "H:/data/"
    basepath_ftr = basepath # +"python_pandas/VEKTIS/"

    year = 2020

    yearstr = str(year)
    filename_core = "MSZPrestatiesVEKT" + yearstr +"_cc"
    i_start = 0 
    i = i_start
    end_i = 150
    i_step = 50
    filename = basepath_ftr + filename_core + "_" + str(i) + ".ftr"    
    start = time.time()    
    file_exists = os.path.exists(filename)
    while file_exists and i<end_i: #  and i<=5
        print("reading " + filename)
        df = pd.read_feather(filename)
        print(df.shape)
        if i == i_start:
            df_total = df
        else:
            df_total = df_total.append(df)
        print(df_total.shape)
        i += i_step
        filename = basepath_ftr + filename_core + "_" + str(i) + ".ftr" 
        file_exists = os.path.exists(filename)

    df_total.reset_index(inplace=True,drop=True)
    print(time.time() - start)

    filename_core = "MSZPrestatiesVEKT" + yearstr

    basepath_out = "H:/data/"
    basepath_ftr_out = basepath_out + "python_pandas/VEKTIS/"
    basepath_csv_out = basepath_out + "csv/VEKTIS/"

    filename_csv =  basepath_csv_out+filename_core+"_total_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df_total.head(100).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr_out +filename_core +"_total.ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df_total.to_feather(filename_ftr)
    print(time.time() - start)

    
    
if __name__ == '__main__':
    run_main()
    