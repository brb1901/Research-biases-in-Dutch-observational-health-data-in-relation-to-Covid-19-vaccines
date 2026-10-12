from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = "G:/GezondheidWelzijn/GEBWLZTAB/"
    basepath_dta = basepath+"stata/WLZ/"
    basepath_ftr = basepath+"python_pandas/WLZ/"
    basepath_csv = basepath+"csv/WLZ/"

    basepath_ext_sav = basepath_sav
    filename_core_other = "gebwlz2018"
    filename_core_sav = filename_core_other + "tabv1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav
    filename_core_other = "gebwlz2019"
    filename_core_sav = filename_core_other + "tabv1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav
    filename_core_other = "gebwlz2020"
    filename_core_sav = filename_core_other + "tabv1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav
    filename_core_other = "gebwlz2021"
    filename_core_sav = filename_core_other + "tabv1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)
