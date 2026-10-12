from generic_functions import convert_spss_chunks # convert_spss, convert_spsscsv, 


def run_main():
    basepath = "H:/data/"
    basepath_sav =  "G:/GezondheidWelzijn/" # "T:/" #
    basepath_dta = basepath+"stata/VEKTIS/"
    
    basepath_csv = basepath+"csv/VEKTIS/"

    # use_cols = ['RINPERSOON', 'VEKTMSZKoppelIDPrestZa', 'VEKTMSZBegindatumPrest', 'VEKTMSZEinddatumPrest', 'VEKTMSZZorgtrajectnummer', 'VEKTMSZAantalPrest', 
    #              'VEKTMSZZorgtype', 'VEKTMSZSpecialismeDiagnoseCombinatie', 'VEKTMSZDBCZorgproduct', 'VEKTMSZVergoedbedragZVW', 'VEKTMSZVergoedbedragAV', 
    #              'VEKTMSZSoortinstelling4cat', 'VEKTMSZSettingZPK', 'VEKTMSZAfsluitreden','VEKTMSZVerwijzer', 'VEKTMSZSpecialismeVerwijzer']

    # basepath_ext_sav = basepath_sav+"MSZZORGACTIVITEITENVEKTTAB2021/"
    # filename_core_other = "MSZZorgactiviteitenVEKT2021"
    # filename_core_sav = filename_core_other+"TABV1"  
    # basepath_ftr = basepath+"python_pandas/VEKTIS/2021/"  
    # convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=None, chunksiz=5000000)

    basepath_ext_sav = basepath_sav+"MSZZORGACTIVITEITENVEKTTAB2020/"
    filename_core_other = "MSZZorgactiviteitenVEKT2020"
    filename_core_sav = filename_core_other+"TABV2"  
    basepath_ftr = basepath+"python_pandas/VEKTIS/2020/"  
    convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=None, chunksiz=5000000)

    basepath_ext_sav = basepath_sav+"MSZZORGACTIVITEITENVEKTTAB/2019/"
    filename_core_other = "MSZZorgactiviteitenVEKT2019"
    filename_core_sav = filename_core_other+"TABV2"  
    basepath_ftr = basepath+"python_pandas/VEKTIS/2019/"  
    convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=None, chunksiz=5000000)

    basepath_ext_sav = basepath_sav+"MSZZORGACTIVITEITENVEKTTAB/2018/"
    filename_core_other = "MSZZorgactiviteitenVEKT2018"
    filename_core_sav = filename_core_other+"TABV2"  
    basepath_ftr = basepath+"python_pandas/VEKTIS/2018/"  
    convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=None, chunksiz=5000000)


if __name__ == '__main__':
    run_main()
    