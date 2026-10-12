import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    basepath = "C:/Users/bramb/datastore/tech/projects/Oversterfte_PostCovid/"
    path_loadsave = basepath + "export_uit_CBS/260707_0500_export_4C_proj3023/export_4C_proj3023/surv_curves/"
    # path_loadsave = basepath + "export_uit_CBS/250211_0500_to_export_5/to_export_5/txt_csv_python/surv_curves/"
    # path_loadsave = basepath + "export_uit_CBS/260904_0500_LIGHT_export_5_proj3023/export_5_proj3023/surv_curves/"

    filename_core = "surv_curve_vax1_morttype1_1940-1950_WLZbit1_RxRisk-1_v3B"
    # surv_curve_vax0_morttype1_1950-1960_WLZbit0_RxRisk-1_v3.csv
    # filename_core = "surv_curve_vax1_morttype1_1950-1960_WLZbit0_RxRisk-1_v3"
    # filename_core = "surv_curve_vax0_morttype1_1940-1950_WLZbit1_RxRisk-1_v3"
    # filename_core = "surv_curve_vax1_morttype2_1960-1980_WLZbit0_RxRisk-1_v3"
    # filename_core = "surv_curve_vax-1_morttype2_2000-2020_WLZbit0_RxRisk-1_v7B"

    filename_csv = path_loadsave + filename_core+".csv"
    print("reading: " + filename_core)

    # df = pd.read_csv(filename_csv)
    df = pd.read_csv(filename_csv, delimiter=";", decimal=",") # voor: 250211_0500_to_export_5/to_export_5  !!
    # df = pd.read_csv(filename_csv, delimiter=",", decimal=".") # voor: 260904_0500_LIGHT_export_5_proj3023/export_5_proj3023 en ik denk ook 260707_0500_export_4C_proj3023/export_4C_proj3023/  !!
    print(df.shape)
    # length = len(df)
    # print(length)
    colname = df.columns[1]
    print(colname)
    maxval = int(df["timeline"].max())
    print(maxval)

    df2 = pd.DataFrame()
    df2["timeline"] = range(maxval+1)  # (length)
    # df2[colname] = -1.0

    df3 = pd.merge(df2, df, how='outer', on=["timeline"])

    prevval = 1
    for index, rowdata in df3.iterrows():
        val = rowdata[colname]
        if np.isnan(val): # or val == 0.0:
            df3.at[index,colname]=prevval
        else:
            prevval = val
    
    filename_core =  filename_core + "_interp"
    filename_csv = path_loadsave + filename_core  +".csv"

    print("writing: "+filename_csv)
    df3.to_csv(filename_csv) # , float_format='%8.2f'
