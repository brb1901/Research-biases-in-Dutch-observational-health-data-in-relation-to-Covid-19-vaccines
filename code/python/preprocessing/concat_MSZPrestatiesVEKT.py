import os
import pandas as pd
import time

def run_main():
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    year = 2018

    yearstr = str(year)
    filename_core = "MSZPrestatiesVEKT" + yearstr 
    
    
    i_start = 0 
    file_exists = True
    while file_exists:
        i = i_start
        end_i = i_start + 50
        filename = basepath_ftr + yearstr + "/" + filename_core + "_" + str(i) + ".ftr"    
        start = time.time()    
        file_exists = os.path.exists(filename)
        new_files = False
        while file_exists and i<end_i: #  and i<=5
            new_files = True
            print("reading " + filename)
            df = pd.read_feather(filename)
            print(df.shape)
            if i == i_start:
                df_total = df
            else:
                df_total = df_total.append(df)
            print(df_total.shape)
            i += 1
            filename = basepath_ftr + yearstr + "/" + filename_core + "_" + str(i) + ".ftr"       
            file_exists = os.path.exists(filename)

        if new_files:
            df_total.reset_index(inplace=True,drop=True)
            print(time.time() - start)

            filename_csv =  basepath_csv+filename_core+"_cc_" + str(i_start) + "_head.csv"
            print("writing (head): "+filename_csv)
            start = time.time()
            df_total.head(100).to_csv(filename_csv)
            print(time.time() - start)

            filename_ftr = basepath_ftr +filename_core +"_cc_" + str(i_start) +".ftr"
            print("writing: "+filename_ftr)
            start = time.time()
            df_total.to_feather(filename_ftr)
            print(time.time() - start)

            i_start = i_start + 50

    
    
if __name__ == '__main__':
    run_main()
    