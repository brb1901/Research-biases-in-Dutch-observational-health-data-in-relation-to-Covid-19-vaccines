from generic_functions import convert_spss

if __name__ == '__main__':
    basepath = "H:/data/"
    basepath_sav = "G:/Bevolking/" # basepath+"spss_sav/GBA/" 
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    use_cols = ['RINPERSOON','GBAGEBOORTELAND','GBAGEBOORTELANDMOEDER','GBAGEBOORTELANDVADER','GBAGESLACHT','GBAGEBOORTEJAAR','GBAGEBOORTEMAAND']

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2012/"
    # filename_core_other = "GBAPERSOON2012"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2013/"
    # filename_core_other = "GBAPERSOON2013"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2014/"
    filename_core_other = "GBAPERSOON2014"
    filename_core_sav = filename_core_other+"TABV1"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2015/"
    filename_core_other = "GBAPERSOON2015"
    filename_core_sav = filename_core_other+"TABV1"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2016/"
    filename_core_other = "GBAPERSOONTAB2016" # bizar!
    filename_core_sav = filename_core_other+"V1"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)
    # #DEBUG must rename resulting ftr file!!

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2017/"
    # filename_core_other = "GBAPERSOON2017"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2018/"
    # filename_core_other = "GBAPERSOON2018"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2019/"
    # filename_core_other = "GBAPERSOON2019"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2020/"
    # filename_core_other = "GBAPERSOON2020"
    # filename_core_sav = filename_core_other+"TABV3"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2021/"
    # filename_core_other = "GBAPERSOON2021"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)

    # basepath_ext_sav = basepath_sav+"GBAPERSOONTAB/2022/"
    # filename_core_other = "GBAPERSOON2022"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols)


