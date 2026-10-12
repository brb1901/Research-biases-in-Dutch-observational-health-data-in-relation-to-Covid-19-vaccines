import pandas as pd
import time
# from datetime import date
import matplotlib.pyplot as plt


def run_main():
    basepath = "H:/data/"
    # basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    print("reading GBAOVERLIJDEN2022_ext feather data")
    # start = time.time()
    df_o = pd.read_feather(basepath_ftr+"GBAOVERLIJDEN2022_ext.ftr")
    # print(time.time() - start)
    # print(df_o.shape)

    dDict = {}
    labelList =[]
    nrAgeGrDict = {}
    nfactorDict = {}
    for year in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]:
        yearstr = str(year)
        print(yearstr)

        print("selecting deaths in " + yearstr)
        df_f = df_o[df_o["jaar_overlijden"] == year]
        df_f.reset_index(inplace=True,drop=True)
        # print(df_f.shape)
        dDict[yearstr] = df_f['leeftijd_overlijden']
        labelList.append(yearstr)

        yearstr_prev = str(year-1)
        print("reading GBAPERSOON_ext" + yearstr_prev + " feather data")
        # start = time.time()
        df_p = pd.read_feather(basepath_ftr+"GBAPERSOON" + yearstr_prev + "_presentalivethatwholeyear.ftr")
        # print(time.time() - start)
        # print(df_p.shape)

        nr_p_agList = []
        nfactorList = []
        for age in range(0,110,10):
            age_from = max(0,age-1)
            age_to = age+10-1
            nr_p_ag = len( df_p[ (df_p['leeftijd_in_ditjaar']>=age_from) & (df_p['leeftijd_in_ditjaar']<age_to) ] )
            nr_p_agList.append(nr_p_ag)
            nfactor = float(nr_p_ag)/100000.0
            nfactorList.append(nfactor)
            print(str(age) + " " + str(age_to+1) + " " + str(nr_p_ag) + " " + str(nfactor))
            
        nrAgeGrDict[yearstr] = nr_p_agList
        nfactorDict[yearstr] = nfactorList
        print()

        

    # plt.ion()
    # plt.hist(df_f['leeftijd_overlijden'], bins=range(0,120,5))
    plt.hist([dDict['2015'], dDict['2016'], dDict['2017'], dDict['2018'], dDict['2019'], dDict['2020'], dDict['2021'], dDict['2022']], bins=range(0,120,10), label=labelList)
    plt.xlabel('age')
    plt.ylabel('number of deaths')
    plt.xticks(range(0,120,10))
    plt.legend()
    plt.title("Deaths per age group, multiple years, NL")
    versionstr = "_v1"
    # plt.savefig("H:/data/plots/hist_deaths_multyears" + versionstr + ".pdf", format="pdf", bbox_inches="tight")
    # plt.savefig("H:/data/plots/hist_deaths_" + yearstr + ".pdf", format="pdf", bbox_inches="tight")
    plt.show() # block=False


if __name__ == '__main__':
    run_main()
    


 