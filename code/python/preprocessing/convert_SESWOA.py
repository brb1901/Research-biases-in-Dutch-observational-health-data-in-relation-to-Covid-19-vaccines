from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = "G:/Bevolking/SESWOA/"
    basepath_dta = basepath+"stata/SESWOA/"
    basepath_ftr = basepath+"python_pandas/SESWOA/"
    basepath_csv = basepath+"csv/SESWOA/"

    # basepath_ext_sav = basepath_sav
    # filename_core_other = "SESWOA2018"
    # filename_core_sav = filename_core_other+"V2"
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav
    # filename_core_other = "SESWOA2019"
    # filename_core_sav = filename_core_other+"V2"
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav
    filename_core_other = "SESWOA2020"
    filename_core_sav = filename_core_other+"V1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav
    # filename_core_other = "SESWOA2021"
    # filename_core_sav = filename_core_other+"V1"
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)
