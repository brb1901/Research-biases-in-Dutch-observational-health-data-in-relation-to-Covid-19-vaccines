import pandas as pd
import os
import csv
# from xlsxwriter.workbook import Workbook

def process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, booster=False):
    basepath = "H:/data/"
    basepath_csv = basepath+"to_export_2e/txt_csv_python/" + mat_str +"/"
    basepath_csv_out = basepath+"to_export_2e/txt_csv_python/" + mat_str +"/"
    # basepath_csv = basepath+"output/csv_python/ves/" + mat_str +"/"
    # basepath_csv_out = basepath+"output/csv_python/ves/" + mat_str +"/"
    filename_core = "ve_etc_" + mat_str + "_" + yearsstr + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + "_WLZlevel" + str(wlz_levels) + versionstr 
    
    if booster:
        filename_core += "_BOOSTER"

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
    
    mat_str = "matched" #  "unmatched_dotter" #   "unmatched" # 
    stepsize = 10
    versionstr = "_v3E" #   "_v0E" # 
    yearsstr = "2021-2023"
    wlz_bit = 0
    booster = True # False # 

    for birthyear in range(1920,2011,stepsize):
    # stepsize = 100
    # for birthyear in range(1910,2009,stepsize):
        birthyear_from = birthyear
        birthyear_to = birthyear_from + stepsize
        # age_from = refyear - birthyear_to
        # age_to = refyear - birthyear_from
        print(birthyear_from)
        print(birthyear_to)
        print()

        for wlz_bit in [0,1]:
            # print(wlz_bit)

            if wlz_bit==0:
                wlz_levels = -1
                for med_rxrisk_scores in [-1,0,1]:
                    process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, booster)
            else:
                med_rxrisk_scores = -1
                for wlz_levels in [-1,0,1]:
                    process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, booster)

    stepsize = 20
    for birthyear in range(1920,2011,stepsize):
    # stepsize = 100
    # for birthyear in range(1910,2009,stepsize):
        birthyear_from = birthyear
        birthyear_to = birthyear_from + stepsize
        # age_from = refyear - birthyear_to
        # age_to = refyear - birthyear_from
        print(birthyear_from)
        print(birthyear_to)
        print()

        for wlz_bit in [0,1]:
            # print(wlz_bit)

            if wlz_bit==0:
                wlz_levels = -1
                for med_rxrisk_scores in [-1,0,1]:
                    process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, booster)
            else:
                med_rxrisk_scores = -1
                for wlz_levels in [-1,0,1]:
                    process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, booster)
        

if __name__ == '__main__':
    run_main()
    
