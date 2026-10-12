from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = "G:/GezondheidWelzijn/MEDICIJNTAB/"
    basepath_dta = basepath+"stata/MEDICIJN/"
    basepath_ftr = basepath+"python_pandas/MEDICIJN/"
    basepath_csv = basepath+"csv/MEDICIJN/"

    basepath_ext_sav = basepath_sav+ "2018/"
    filename_core_other = "MEDICIJN2018"
    filename_core_sav = filename_core_other+"TABV1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav+ "2019/"
    filename_core_other = "MEDICIJN2019"
    filename_core_sav = filename_core_other+"TABV1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav+ "2020/"
    filename_core_other = "MEDICIJN2020"
    filename_core_sav = filename_core_other+"TABV2"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+ "2021/"
    # filename_core_other = "MEDICIJN2021"
    # filename_core_sav = filename_core_other+"TABV1"
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)
