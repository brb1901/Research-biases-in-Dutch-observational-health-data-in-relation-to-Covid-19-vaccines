import pandas as pd
import os
import csv
# from xlsxwriter.workbook import Workbook

def run_main():
    basepath = "H:/data/"
    basepath_csv = basepath+"to_export_2/txt_csv_python/matched/"
    basepath_csv_out = basepath+"to_export_2b/txt_csv_python/matched/"

    mat_str = "matched"
    stepsize = 10
    versionstr = "_v3"
    yearsstr = "2021-2023"
    wlz_bit = 0
    wlz_levels = -1
    med_rxrisk_scores = -1

    birthyear_from = 1940
    birthyear_to = birthyear_from + stepsize
    filename_core = "ve_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + versionstr 
    
    filename_csv = basepath_csv+filename_core+".csv"
    if os.path.exists(filename_csv):
        print("reading: " + filename_core)
        df = pd.read_csv(filename_csv)                

        # filename_xls = basepath_csv+filename_core+".xlsx"
        # print("writing: "+filename_xls)
        # df.to_excel(filename_xls)
        filename_csv_out = basepath_csv_out+filename_core+".csv"
        print("writing: "+filename_csv_out)
        df.to_csv(filename_csv_out, sep =';', encoding='ANSI', index=False, decimal=",")
        

if __name__ == '__main__':
    run_main()
    
