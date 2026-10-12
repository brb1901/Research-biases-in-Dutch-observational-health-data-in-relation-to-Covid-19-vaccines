import pandas as pd
# import pyreadstat
# import time
# import gc

def read_population_generic(filename_core):
    basepath = "H:/data/"    
    print("reading " + filename_core + " csv data")
    df_pop = pd.read_csv(basepath+"csv/populatie/" + filename_core + ".csv")
    return df_pop

def read_population_NL_all():
    filename_core = "PopulatieNederland_CBSgebaseerd_perleeftijd_TOTAAL_v2"
    df_pop = read_population_generic(filename_core)
    return df_pop

def read_population_NL_men():
    filename_core = "PopulatieNederland_CBSgebaseerd_perleeftijd_MANNEN_v2"
    df_pop = read_population_generic(filename_core)
    return df_pop

def read_population_NL_women():
    filename_core = "PopulatieNederland_CBSgebaseerd_perleeftijd_VROUWEN_v2"
    df_pop = read_population_generic(filename_core)
    return df_pop

def get_nr_people_fromto_age(df_pop, year, age_from_incl, age_to_excl):
    data_year = df_pop.loc[(df_pop["leeftijdscat_jaar_aantal"]>=age_from_incl) & (df_pop["leeftijdscat_jaar_aantal"]<age_to_excl), str(year)]
    # print(data_year)
    # print(data_year.sum())
    return data_year.sum()


