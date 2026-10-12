import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    basepath = "C:/Users/bramb/bakkerrepo/techrepo/projects/Oversterfte/excel/"

    # filename_core = "QBA2_VB_Ooutput_ACM_1940_1950_WLZ0_v1"
    # filename_core = "QBA1_Output_1940_1950_WLZ0_V5A_mixed"
    # filename_core = "QBA1_Output_1940_1950_WLZ0_V5A_COVIDUNREALISTIC" # 
    # QBA1_Output_1940_1950_WLZ0_V5A_EXTREMEHVE
    filename_core = "QBA1_Output_1940_1950_WLZ0_V5A_EXTREMEHVE" # 

    filename_csv = basepath + filename_core+".csv"
    print("reading: " + filename_core)
    df = pd.read_csv(filename_csv)
    print(df.shape)

    # df["unvac_offset_low"] = df["ACM Unvaccinated_lower_0.95"] - df["ACM Unvaccinated"]
    # df["unvac_offset_up"] = df["ACM Unvaccinated_upper_0.95"] - df["ACM Unvaccinated"]

    # df["unvac_offset_low"] = df["unvac_offset_low"]*2
    # df["unvac_offset_up"] = df["unvac_offset_up"]*3

    # df["vac_offset_low"] = df["ACM Vaccinated_lower_0.95"] - df["ACM Vaccinated"]
    # df["vac_offset_up"] = df["ACM Vaccinated_upper_0.95"] - df["ACM Vaccinated"]

    # df["vac_offset_low"] = df["vac_offset_low"]*3
    # df["vac_offset_up"] = df["vac_offset_up"]*2

    # df["ACM_corr_unvac_low"] = df["ACM Unvaccinated"] + df["unvac_offset_low"]
    # df["ACM_corr_unvac_up"] = df["ACM Unvaccinated_corrected"] + df["unvac_offset_up"]
    # df["ACM_corr_unvac_up"] = df["ACM_corr_unvac_up"].clip(upper=1)

    # df["ACM_corr_vac_low"] = df["ACM Vaccinated_corrected"] + df["vac_offset_low"]
    # df["ACM_corr_vac_up"] = df["ACM Vaccinated"] + df["vac_offset_up"]
    # df["ACM_corr_vac_up"] = df["ACM_corr_vac_up"].clip(upper=1)

    x = df["timeline"]

    # y = df["ACM Vaccinated"]
    y = df["MEASURED ACM Vaccinated"]
    plt.plot(x, y, linestyle='-', color='tab:orange', label="Meas. Vacc. ACM")
    # y = df["ACM Vaccinated_corrected"]
    y = df["SIMULATED ACM Vaccinated"]
    plt.plot(x, y, linestyle=':', linewidth='2', color='tab:orange', label="Sim. Vacc. ACM \"Extreme HVE\"")
    # plt.fill_between(x, df["ACM_corr_vac_low"], df["ACM_corr_vac_up"], 
    #              color='tab:orange', 
    #              alpha=0.3,
    #              label='Vacc. Total Error Interval')  # transparency (0.0 to 1.0) ,label='95% Confidence Interval'
                 

    # y = df["ACM Unvaccinated"]
    y = df["MEASURED ACM Unvaccinated"]
    plt.plot(x, y, linestyle='-', color='tab:blue', label="Meas. Unvacc. ACM")
    # y = df["ACM Unvaccinated_corrected"]
    y = df["SIMULATED ACM Unvaccinated"]
    plt.plot(x, y, linestyle=':', linewidth='2', color='tab:blue', label="Sim. Unvacc. ACM \"Extreme HVE\"")
    # plt.fill_between(x, df["ACM_corr_unvac_low"], df["ACM_corr_unvac_up"], 
    #              color='tab:blue', 
    #              alpha=0.3,
    #              label='Unvacc. Total Error Interval')  # transparency (0.0 to 1.0) ,label='95% Confidence Interval'


    plt.axis((-10, 760, 0.760, 1.02))

    versionstr = "_v5a"
    birthyear_from = 1940
    birthyear_to = 1950
    wlz_bit = 0
    med_rxrisk_scores = -1
    scenarioname = "QBA1, ACM, " + versionstr
    # plt.title("Scenario " + scenarioname + str(birthyear_from) + "-" + str(birthyear_to) + ", WLZ " + str(wlz_bit)+ ", RxRisk " + str(med_rxrisk_scores) + ", " + versionstr)
    plt.ylabel("probability of survival")
    plt.xlabel("time since treatment (days)")
    # plt.legend()
    plt.legend(loc = 'lower left')

    # plt.plot(yq, nr0, "ko-", label="2018")
    # plt.plot(yq, nr1, "bo-", label="2019")
    # plt.plot(yq, nr2, "ro-", label="2020")
    # plt.plot(yq, nr3, "go-", label="2021")
    # plt.axis((0, 5, 3000, 6500))
    # plt.xlabel("year quarter")
    # plt.ylabel("number of operations")
    # plt.legend()

    scenarioname = "QBA1_Output_ACM_ExtremeHVE_"
    filename_core = scenarioname + str(birthyear_from) + "-" + str(birthyear_to) + "_WLZ" + str(wlz_bit)+ "RxRisk" + str(med_rxrisk_scores) + versionstr
    filename_fig = basepath + "plots/" + filename_core + ".pdf"
    plt.savefig(filename_fig, format="pdf", bbox_inches="tight")

    plt.show()

