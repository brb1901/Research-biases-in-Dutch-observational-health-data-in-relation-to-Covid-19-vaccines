from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = basepath+"spss_sav/GGDCOVID19/"
    basepath_dta = basepath+"stata/GGDCOVID19/"
    basepath_ftr = basepath+"python_pandas/GGDCOVID19/"
    basepath_csv = basepath+"csv/GGDCOVID19/"

    basepath_ext_sav = basepath_sav
    filename_core_other = "HPZonedata_2020"
    filename_core_sav = filename_core_other+"V1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav
    filename_core_other = "HPZonedata_2021"
    filename_core_sav = filename_core_other+"V1"
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)
