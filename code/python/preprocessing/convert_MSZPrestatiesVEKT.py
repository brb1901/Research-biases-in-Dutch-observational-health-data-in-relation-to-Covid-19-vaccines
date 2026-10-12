from generic_functions import convert_spss_chunks # convert_spss, convert_spsscsv, 


def run_main():
    basepath = "H:/data/"
    basepath_sav =  "G:/GezondheidWelzijn/" # "T:/" #
    basepath_dta = basepath+"stata/VEKTIS/"
    basepath_ftr = basepath+"python_pandas/VEKTIS/"
    basepath_csv = basepath+"csv/VEKTIS/"

    use_cols = ['RINPERSOON', 'VEKTMSZKoppelIDPrestZa', 'VEKTMSZBegindatumPrest', 'VEKTMSZEinddatumPrest', 'VEKTMSZZorgtrajectnummer', 'VEKTMSZAantalPrest', 
                 'VEKTMSZZorgtype', 'VEKTMSZSpecialismeDiagnoseCombinatie', 'VEKTMSZDBCZorgproduct', 'VEKTMSZVergoedbedragZVW', 'VEKTMSZVergoedbedragAV', 
                 'VEKTMSZSoortinstelling4cat', 'VEKTMSZSettingZPK', 'VEKTMSZAfsluitreden','VEKTMSZVerwijzer', 'VEKTMSZSpecialismeVerwijzer']

    basepath_ext_sav = basepath_sav+"MSZPRESTATIESVEKTTAB/2018/"
    filename_core_other = "MSZPrestatiesVEKT2018"
    filename_core_sav = filename_core_other+"TABV3"    
    convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols, chunksiz=10000)

    # basepath_ext_sav = basepath_sav+"MSZPRESTATIESVEKTTAB/2019/"
    # filename_core_other = "MSZPrestatiesVEKT2019"
    # filename_core_sav = filename_core_other+"TABV3"    
    # convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols, chunksiz=1000000)

    # basepath_ext_sav = basepath_sav+"MSZPRESTATIESVEKTTAB2020/"
    # filename_core_other = "MSZPrestatiesVEKT2020"
    # filename_core_sav = filename_core_other+"TABV3"    
    # convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols, chunksiz=1000000)

    # basepath_ext_sav = basepath_sav+"MSZPRESTATIESVEKTTAB2021/"
    # filename_core_other = "MSZPrestatiesVEKT2021"
    # filename_core_sav = filename_core_other+"TABV1"    
    # convert_spss_chunks(basepath_ext_sav,filename_core_sav,filename_core_other,basepath_ftr,basepath_dta,basepath_csv, usecols=use_cols, chunksiz=1000000)

if __name__ == '__main__':
    run_main()
    