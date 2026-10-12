import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    basepath = "C:/Users/bramb/datastore/tech/projects/Oversterfte_PostCovid/"

    filename_core = "QBA2_VB_Ooutput_NC_asjustmentfactors_1940_1950_WLZ0_v1"

    filename_csv = basepath+ "QBA/" +filename_core+".csv"
    print("reading: " + filename_core)
    df = pd.read_csv(filename_csv)
    print(df.shape)

    x = df["timeline"]

    y = df["deathrate_V_MA3"]
    plt.plot(x, y, linestyle='-', color='tab:orange', label="Vacc. Non-Covid Death Rate")
    y = df["deathrate_U_MA3"]
    plt.plot(x, y, linestyle='-', color='tab:blue', label="Unvacc. Non-Covid Death Rate")
    # plt.xscale('log')   # x-axis logarithmic
    y = df["deathrate_A_MA3"]
    plt.plot(x, y, linestyle='-', color='tab:green', label="Overall Non-Covid Death Rate")
    plt.yscale('log')   # y-axis logarithmic

    

    # plt.axis((-10, 810, 0.82, 1.015))

    # plt.arrow(190,0.894,0,0.078, length_includes_head=True, head_width=0.1, head_length=0.01) # , length_includes_head=True, head_width=0.2, head_length=0.0002 , color = 'tab:black'

    # plt.annotate('',xy=(253,0.978),xytext=(266,.9846),arrowprops={'arrowstyle':'->'}, horizontalalignment='center',color = 'tab:orange') # Adjustment Vaccinated ,"width":2,"headwidth":5
    # plt.annotate('',xy=(299,0.9769),xytext=(238,0.8846),arrowprops={'arrowstyle':'->'}, horizontalalignment='center',color = 'tab:blue') # Adjustment Unvaccinated ,"width":2,"headwidth":5
    # plt.annotate(r'$\downarrow$ adjustment'+ '\nvaccinated',xy=(253,0.978),xytext=(276,.9890),rotation=-10,arrowprops=dict(arrowstyle='->', color='tab:orange'), horizontalalignment='center',color = 'tab:orange') # Adjustment Vaccinated ,"width":2,"headwidth":5
    # plt.annotate(r'$\uparrow$ adjustment'+ '\nunvaccinated',xy=(279,0.9779),xytext=(190,0.8550),rotation=-20,arrowprops=dict(arrowstyle='->', color='tab:blue'), horizontalalignment='center',color = 'tab:blue') # Adjustment Unvaccinated ,"width":2,"headwidth":5
        

    versionstr = "_v3B"
    birthyear_from = 1940
    birthyear_to = 1950
    wlz_bit = 0
    med_rxrisk_scores = -1
    scenarioname = "QBA2 Version B, "
    # plt.title("Scenario " + scenarioname + str(birthyear_from) + "-" + str(birthyear_to) + ", WLZ " + str(wlz_bit)+ ", RxRisk " + str(med_rxrisk_scores) + ", " + versionstr)
    plt.ylabel("death rate per day (log scale)")
    plt.xlabel("time since treatment (days)")
    plt.legend()
    # plt.legend(loc = 'lower left')

    # plt.plot(yq, nr0, "ko-", label="2018")
    # plt.plot(yq, nr1, "bo-", label="2019")
    # plt.plot(yq, nr2, "ro-", label="2020")
    # plt.plot(yq, nr3, "go-", label="2021")
    # plt.axis((0, 5, 3000, 6500))
    # plt.xlabel("year quarter")
    # plt.ylabel("number of operations")
    # plt.legend()

    scenarioname = "QBA2_VersionB_NC_deathrates_logscale_"
    filename_core = scenarioname + str(birthyear_from) + "-" + str(birthyear_to) + "_WLZ" + str(wlz_bit)+ "RxRisk" + str(med_rxrisk_scores) + versionstr
    filename_fig = basepath + "QBA/plots/" + filename_core + ".pdf"
    plt.savefig(filename_fig, format="pdf", bbox_inches="tight")

    plt.show()

