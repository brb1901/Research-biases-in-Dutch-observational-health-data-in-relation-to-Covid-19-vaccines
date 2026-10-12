import os
import pandas as pd
import time

def run_main():
    basepath = "H:/data/csv/diagnosethesaurus/" 
    filename_core = "20231016_095421_uitleverformaat4.3_VT_BronZA"   
    print("reading " + filename_core + " csv data")
    # df_AflDBC = pd.read_csv(basepath + filename_core + ".csv")
    df_BronZA = pd.read_csv(basepath + filename_core + ".csv", dtype=str, keep_default_na=False)
    
    df_BronZA_un = df_BronZA.drop_duplicates(subset = "ZPK_omschrijving")

    use_cols = ["ZPK_code","ZPK_omschrijving"]
    df_BronZA_un = df_BronZA_un[use_cols]
    df_BronZA_un.reset_index(inplace=True,drop=True)

    print(df_BronZA_un)

    filename_csv = basepath + "BronZA_uniquecategoriesZPK.csv"
    print("writing: "+filename_csv)
    df_BronZA_un.to_csv(filename_csv)
    
if __name__ == '__main__':
    run_main()
    