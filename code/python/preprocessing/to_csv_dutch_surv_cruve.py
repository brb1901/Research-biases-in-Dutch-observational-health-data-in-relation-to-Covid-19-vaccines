import pandas as pd
import os
import csv
# from xlsxwriter.workbook import Workbook

def process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, vax, morttype):
    basepath = "H:/data/"
    basepath_csv = basepath+"to_export_2/txt_csv_python/surv_curves/"
    basepath_csv_out = basepath+"to_export_2b/txt_csv_python/surv_curves/"
    filename_core = "surv_curve_vax" + str(vax) + "_morttype" +str(morttype) + "_" + str(birthyear_from) +"-" + str(birthyear_to) +"_WLZbit" + str(wlz_bit) +"_RxRisk" + str(med_rxrisk_scores) + versionstr 


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
    
    mat_str ="matched" #  "unmatched_dotter" # "unmatched" # "matched"
    stepsize = 10
    versionstr = "_v3"
    yearsstr = "2021-2023"
    wlz_bit = 0
    # booster = False

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
                    for vax in [0,1]:
                        for morttype in [0,1,2]:
                            process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, vax, morttype)
            else:
                med_rxrisk_scores = -1
                # for wlz_levels in [-1,0,1]:
                wlz_levels = -1
                for vax in [0,1]:
                    for morttype in [0,1,2]:
                        process_file(yearsstr, birthyear_from, birthyear_to, wlz_bit, med_rxrisk_scores, wlz_levels, mat_str, versionstr, vax, morttype)

        
        

if __name__ == '__main__':
    run_main()
    
