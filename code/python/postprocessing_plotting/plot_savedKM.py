import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    basepath = "C:/Users/bramb/datastore/tech/projects/Oversterfte_PostCovid/"

    filename_core = "QBA1_scenario_mixed_1"

    filename_csv = basepath+ "QBA/" +filename_core+".csv"
    print("reading: " + filename_core)
    df = pd.read_csv(filename_csv)
    print(df.shape)

    labelstr = "MEASURED ACM Unvaccinated"
    df[labelstr].plot(style='-', color='blue', label=labelstr)
    labelstr = "MEASURED ACM Vaccinated"
    df[labelstr].plot(style='-', color='orange', label=labelstr)
    labelstr = "SIMULATED ACM Unvaccinated"
    df[labelstr].plot(style='-', color='green', label=labelstr)
    labelstr = "SIMULATED ACM Vaccinated"
    df[labelstr].plot(style='-', color='red', label=labelstr)

    plt.axis((-10, 780, 0.75, 1.02))

    versionstr = "_v3"
    birthyear_from = 1940
    birthyear_to = 1950
    wlz_bit = 0
    med_rxrisk_scores = -1
    scenarioname = "mixed_1, "
    plt.title("Scenario " + scenarioname + str(birthyear_from) + "-" + str(birthyear_to) + ", WLZ " + str(wlz_bit)+ ", RxRisk " + str(med_rxrisk_scores) + ", " + versionstr)
    plt.ylabel("probability of survival")
    plt.xlabel("time since treatment (days)")
    plt.legend(loc = 'lower left')

    # plt.plot(yq, nr0, "ko-", label="2018")
    # plt.plot(yq, nr1, "bo-", label="2019")
    # plt.plot(yq, nr2, "ro-", label="2020")
    # plt.plot(yq, nr3, "go-", label="2021")
    # plt.axis((0, 5, 3000, 6500))
    # plt.xlabel("year quarter")
    # plt.ylabel("number of operations")
    # plt.legend()

    filename_fig = basepath + "QBA/plots/" + filename_core + versionstr + ".pdf"
    plt.savefig(filename_fig, format="pdf", bbox_inches="tight")

    plt.show()

