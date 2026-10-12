import pandas as pd
import os
import csv
# from xlsxwriter.workbook import Workbook

def process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, weeksteps):
    basepath = "H:/data/"
    basepath_csv = basepath+"to_export_3/txt_csv_python/" + mat_str +"/"
    basepath_csv_out = basepath+"to_export_3/txt_csv_python/" + mat_str +"/"
    # basepath_csv = basepath+"output/csv_python/ves/" + mat_str +"/"
    # basepath_csv_out = basepath+"output/csv_python/ves/" + mat_str +"/"

    # filename_core = "ve_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + versionstr 
    filename_core = "diagn_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels)+ "_W" + str(weeksteps)+ versionstr 

    # if booster:
    #     filename_core += "_BOOSTER"

    filename_csv = basepath_csv+filename_core+".csv"
    # print(filename_csv)
    if os.path.exists(filename_csv):
        print("reading: " + filename_core)
        df = pd.read_csv(filename_csv)                

        # filename_xls = basepath_csv+filename_core+".xlsx"
        # print("writing: "+filename_xls)
        # df.to_excel(filename_xls)
        filename_csv_out = basepath_csv_out+filename_core+".csv"
        print("writing: "+filename_csv_out)
        df.to_csv(filename_csv_out, sep =';', encoding='ANSI', index=False, decimal=",")
    # else:
    #     print("Does not exist. Skipping " + filename_core)

def run_main():
    
    mat_str = "myo_peri_endo_carditis"
    # mat_str = "myocardinfarct"
    weeksteps = 13 # 4 # 

    # stepsize = 10
    versionstr = "_v0" #   "_v0E" # 
    yearsstr = "2018-2021" #  "2021-2023"
    wlz_bit = -1
    med_rxrisk_scores = -1
    wlz_levels = -1
    # booster = False # True # 

    for birthyear in [1940,1960,1980]:
    # stepsize = 100
    # for birthyear in range(1910,2009,stepsize):
        birthyear_from = birthyear
        if birthyear==1940 or birthyear==1960:
            birthyear_to = birthyear_from + 20
        elif birthyear==1980:
            birthyear_to = birthyear_from + 40
        # age_from = refyear - birthyear_to
        # age_to = refyear - birthyear_from
        print(birthyear_from)
        print(birthyear_to)
        print()       

        process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, weeksteps)



if __name__ == '__main__':
    run_main()
    
