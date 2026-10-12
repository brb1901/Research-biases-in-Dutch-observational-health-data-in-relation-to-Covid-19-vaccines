import pandas as pd
import time
from datetime import date
import matplotlib.pyplot as plt


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    print("reading GBAOVERLIJDEN2022_ext feather data")
    # start = time.time()
    df_o = pd.read_feather(basepath_ftr+"GBAOVERLIJDEN2022_ext2.ftr")
    # print(time.time() - start)
    # print(df_o.shape)

    print("reading CIMSDATA_20230801_ext2 feather data")
    df_cims = pd.read_feather(basepath+"python_pandas/CIMS/"+"CIMSDATA_20230801_ext2.ftr")

    # dDict = {}
    # labelList =[]

    # for year in [2018, 2019, 2020, 2021, 2022]:
    # year = 2
    # yearstr = str(year)
    # print(yearstr)

    # print("selecting deaths in " + yearstr)
    # df_f = df_o[df_o["jaar_overlijden"] == year]
    # df_f.reset_index(inplace=True,drop=True)
    # # print(df_f.shape)
    # dDict[yearstr] = df_f['leeftijd_overlijden']
    # labelList.append(yearstr)

    age_from = 0 # 10 # 15 # 60 50
    age_to = 125 # 50 # 45 # 90 75 
    vaxnr = 1

    fromperiod = date(2021,1,1)
    toperiod = date(2021,4,1)
    periodstr = "Jan Feb Mar 2021"

    df_fo = df_o[ (df_o["jaar_overlijden"] >= 2021) & 
                  (df_o["leeftijd_overlijden"] >= age_from) & (df_o["leeftijd_overlijden"] < age_to) ]
    nr_deaths_all = len(df_fo)
    print("Number of deaths in this age group: " + str(nr_deaths_all))

    df_fc = df_cims[  (df_cims["leeftijd_prik"] >= age_from) & (df_cims["leeftijd_prik"] < age_to) &
                         (df_cims["prik_nummer"] == vaxnr) ]
    df_ovax = df_fo[df_fo['RINPERSOON'].isin(df_fc['RINPERSOON'])]
    nr_deaths_vax = len(df_ovax)
    print("Number of deaths (vaccinated) in this age group: " + str(nr_deaths_vax))

    print("\nmerging\n")
    start = time.time()
    df_fc_ext = pd.merge(df_fo, df_fc, how='inner', on=['RINPERSOON'])
    print(time.time() - start)
    print(df_fc_ext)

    days_since_vax = []
    for index, rowdata in df_fc_ext.iterrows():
        if index % 10000 == 0:
            print(index)
        
        datetime_overl = rowdata["datetimeobj_overlijden"]

        if datetime_overl >= fromperiod and datetime_overl < toperiod:
            # rinp_overl = rowdata["RINPERSOON"]
            datetime_prik = rowdata["datetimeobj_prik"]
            days = (datetime_overl-datetime_prik).days
            days_since_vax.append(days)

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    # plt.hist([dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)
    plt.hist(days_since_vax, bins = 20)
    plt.xlabel('days since vaccination')
    plt.ylabel('number of deaths')
    # plt.xticks(range(0,120,10))
    # plt.legend()
    plt.title("Number of deaths, days since vax " + str(vaxnr) + ", " + periodstr + ", age group " + str(age_from) +"-" + str(age_to) )
    versionstr = "_v2"
    # plt.savefig("H:/data/plots/hist_deaths_multyears" + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.savefig("H:/data/plots/hist_days_since_vax" + str(vaxnr) + ", " + periodstr  + "agegroup_" + str(age_from) +"-" + str(age_to)  + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 