from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = basepath+"spss_sav/CIMS/"
    basepath_dta = basepath+"stata/CIMS/"
    basepath_ftr = basepath+"python_pandas/CIMS/"
    basepath_csv = basepath+"csv/CIMS/"

    # basepath_ext_sav = basepath_sav
    # filename_core_other = "CIMSDATA_20230801"
    # filename_core_sav = filename_core_other   
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav
    # filename_core_other = "CIMSDATA_20231003"
    # filename_core_sav = filename_core_other   
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav
    # filename_core_other = "CIMSDATA_20231120"
    # filename_core_sav = filename_core_other   
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav
    filename_core_other = "CIMSDATA_20240124"
    filename_core_sav = filename_core_other   
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)
    