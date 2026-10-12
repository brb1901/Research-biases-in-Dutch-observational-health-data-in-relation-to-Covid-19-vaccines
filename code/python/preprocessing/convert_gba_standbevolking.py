from generic_functions import convert_spss

def run_main():
    basepath = "H:/data/"
    basepath_sav = basepath+"spss_sav/GBA/"
    basepath_dta = basepath+"stata/GBA/"
    basepath_ftr = basepath+"python_pandas/GBA/"
    basepath_csv = basepath+"csv/GBA/"

    # use_cols = ['RINPERSOON','GBAGEBOORTELAND','GBAGEBOORTELANDMOEDER','GBAGEBOORTELANDVADER','GBAGESLACHT','GBAGEBOORTEJAAR','GBAGEBOORTEMAAND']

    basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2014/"
    filename_core_other = "GBASTANDBEVOLKING2014"
    filename_core_sav = filename_core_other+"TABV1"    
    convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2015/"
    # filename_core_other = "GBASTANDBEVOLKING2015"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2016/"
    # filename_core_other = "GBASTANDBEVOLKING2016"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2017/"
    # filename_core_other = "GBASTANDBEVOLKING2017"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2018/"
    # filename_core_other = "GBASTANDBEVOLKING2018"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2019/"
    # filename_core_other = "GBASTANDBEVOLKING2019"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2020/"
    # filename_core_other = "GBASTANDBEVOLKING2020"
    # filename_core_sav = filename_core_other+"TABV2"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2021/"
    # filename_core_other = "GBASTANDBEVOLKING2021"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2022/"
    # filename_core_other = "GBASTANDBEVOLKING2022"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)

    # basepath_ext_sav = basepath_sav+"GBASTANDBEVOLKINGTAB/2023/"
    # filename_core_other = "GBASTANDBEVOLKING2023"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv)


if __name__ == '__main__':
    run_main()
    