from generic_functions import convert_spss

def run_main():
    basepath = "H:/data/"
    basepath_sav = basepath+"spss_sav/DOODOORZ/"
    basepath_dta = basepath+"stata/DOODOORZ/"
    basepath_ftr = basepath+"python_pandas/DOODOORZ/"
    basepath_csv = basepath+"csv/DOODOORZ/"

    # basepath_ext_sav = basepath_sav+"2013/"
    # filename_core_other = "DOODOORZ2013"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2014/"
    # filename_core_other = "DOODOORZ2014"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2015/"
    # filename_core_other = "DOODOORZ2015"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2016/"
    # filename_core_other = "DOODOORZ2016"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2017/"
    # filename_core_other = "DOODOORZ2017"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2018/"
    # filename_core_other = "DOODOORZ2018"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2019/"
    # filename_core_other = "DOODOORZ2019"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2020/"
    # filename_core_other = "DOODOORZ2020"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"2021/"
    # filename_core_other = "DOODOORZ2021"
    # filename_core_sav = filename_core_other+"TABV6"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav+"2022/"
    filename_core_other = "DOODOORZ2022"
    filename_core_sav = filename_core_other+"TABV8"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav+"2023/"
    filename_core_other = "DOODOORZ2023"
    filename_core_sav = filename_core_other+"TABV6"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)


if __name__ == '__main__':
    run_main()
