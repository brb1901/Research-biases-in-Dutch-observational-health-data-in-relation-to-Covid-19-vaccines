from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    # basepath_ext_sav = basepath_sav+"GBAOVERLIJDENTAB/2022/"
    # filename_core_other = "GBAOVERLIJDEN2022"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    basepath_ext_sav = basepath_sav+"GBAOVERLIJDENTAB/2023/"
    filename_core_other = "GBAOVERLIJDEN2023"
    filename_core_sav = filename_core_other+"TABV1"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)
