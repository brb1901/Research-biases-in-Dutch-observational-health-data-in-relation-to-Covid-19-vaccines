import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    basepath = "C:/Users/bramb/datastore/tech/projects/Oversterfte_PostCovid/"

    # filename_core = "QBA1_scenario_mixed_1"
    versionstr = "_v0"
    filename_core =  "data_stringencyindex_confirmedcases_Netherlands"  + versionstr
    filename_csv = basepath+ "QBA/" +filename_core  +".csv"
    print("reading: " + filename_core)
    df1= pd.read_csv(filename_csv)
    print(df1.shape)

    versionstr = "_v0E"
    filename_core =  "year2021_ve_etc_unmatched_1940-1950_WLZbit0_RxRisk-1_WLZlevel-1"  + versionstr
    filename_csv = basepath+ "QBA/" +filename_core  +".csv"
    print("reading: " + filename_core)
    df2= pd.read_csv(filename_csv)
    print(df2.shape)


    df = pd.merge(df1, df2, how='left', on=['m_index'])

    # filename_csv = basepath+ "QBA/" +filename_core+".csv"
    # print("reading: " + filename_core)
    # df = pd.read_csv(filename_csv)
    # print(df.shape)

    x_index = (df["m_index"]+1)*4 

    datastr = "confirmedC19cases4W"
    labelstr = "confirmed Covid cases"
    y = df[datastr]/5500.0
    plt.plot(x_index, y, color='blue', label=labelstr) # style='-', , marker='o'
    datastr = "stringencyindex"
    labelstr = "stringency index"
    y = df[datastr]
    plt.plot(x_index, y, color='black', label=labelstr) # style='-', 
    # nr_deaths_covid_list
    datastr = "nr_deaths_covid_list"
    labelstr = "deaths Covid"
    y = df[datastr]/40.0
    plt.plot(x_index, y, color='cyan', label=labelstr) # style='-', 
    # nr_deaths_list
    datastr = "nr_deaths_list"
    labelstr = "deaths non-Covid"
    y = (df[datastr]-df["nr_deaths_covid_list"])/40.0
    plt.plot(x_index, y, color='red', label=labelstr) # style='-', 

    # nr_deaths_list
    # datastr = "nr_deaths_list"
    labelstr = "vaccinations"
    y = (df["nr_vax1_list"]+df["nr_vax2_list"]+df["nr_vax3_list"])/11000.0
    plt.plot(x_index, y, color='green', label=labelstr) # style='-', 

    plt.xticks(range(0, 52 + 2, 13))
    plt.xlabel("week number in 2021")
    plt.ylabel("scaled data")
    plt.axis((0, 53, 0, 145))
    plt.legend(loc = 'upper left')
    # plt.legend(bbox_to_anchor=(0, 1), loc='upper right', ncol=1)
    # plt.show()

    versionstr = "_v0"
    filename_core =  "calendartimedata_together_confirmedcases_etc"  + versionstr
    filename_fig = basepath + "QBA/plots/" + filename_core + ".pdf"
    plt.savefig(filename_fig, format="pdf", bbox_inches="tight")

    plt.show()

