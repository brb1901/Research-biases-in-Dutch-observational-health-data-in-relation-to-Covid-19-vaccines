import os
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt

def run_main(cat_string):
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath + "csv/VEKTIS/"

    versionstr = "_v0"
    max_rinp_int_file = 1000000000 # 1 miljard  10000000 # 

    # year = int(year_string)
    # year = 2018
    # 
    # yearstr = str(year)
    # print(year)
    firstyear = 2018
    lastyear = 2021

    nr_categories = 10
    x = np.arange(nr_categories)
    wid = 0.03
    multiplier = 0
    nr_YQs = 16 # 12 # 
    nr_items  = nr_YQs
    diagn_number_array = np.zeros(shape=(nr_YQs, nr_categories), dtype=int)

    ICD_cats_list = []
    for j in range(10):
        catsubstr = cat_string + str(j)
        ICD_cats_list.append(catsubstr)

    filename_core =  "VEKTIS_Prest_ZA_diagnosesPerYQ_" + str(firstyear) + "_" + str(lastyear) + "_" + "people_cat_" + str(cat_string) +  versionstr
    filename_ftr = basepath_ftr + "cat_collections/" + filename_core + ".ftr" 
    file_exists = os.path.exists(filename_ftr)
    i=0
    print("computing")
    if file_exists: # True: # 
        df_total = pd.read_feather(filename_ftr)
        for year in [2018, 2019, 2020, 2021]: # 2018, 
            print(year)
            for yq in [1,2,3,4]:
                df_indiv = df_total[ (df_total["year"] == year) & (df_total["quarter"] == yq) ]
                for j in range(10):
                    catsubstr = "cat" + str(j)
                    # print(catsubstr)
                    sumval = df_indiv[catsubstr].sum()
                    # print(sumval)
                    diagn_number_array[i,j] = sumval
                i += 1


    else:
        print("File does not exist!")

    
    i=0
    print("plotting")
    for year in [2018, 2019, 2020, 2021]: # 2018, 
        for yq in [1,2,3,4]:
            offset = wid * multiplier
            multiplier += 1
            plt.bar(x + offset, diagn_number_array[i,:], width=wid, label=str(year)+'_'+str(yq)) # , color = 'b'
            # diagn_number_array[i,j] 
            i += 1

    # plt.title("Causes of death " + yearsstr + ", age group " + str(age_from) +"-" + str(age_to))
    plt.legend()
    # plt.xticks(x + (wid*(float(nr_items)/2.0)), ICD_cats_list)
    plt.xticks(x + (wid*(float(nr_items)/2.0)), ICD_cats_list)
    plt.xlabel('ICD10 codes')
    plt.ylabel('number of diagnoses')

    # plt.savefig("H:/data/output/plots/subcat_" + firstletter_select + "_causes_of_death_" + yearsstr + ", age group " + str(age_from) +"-" + str(age_to) + versionstr + ".pdf", format="pdf", bbox_inches="tight")

    plt.show()
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("cat_string")
    args = parser.parse_args()
    run_main(args.cat_string)
    