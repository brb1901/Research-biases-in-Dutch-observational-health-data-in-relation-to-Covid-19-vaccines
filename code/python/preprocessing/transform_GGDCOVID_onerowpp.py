import math
import pandas as pd
import time


def run_main():
    basepath = "H:/data/"
    basepath_ftr = basepath+"python_pandas/GGDCOVID19/"
    basepath_csv = basepath + "csv/GGDCOVID19/"

    versionstr = "_v0"

    yearstr = "2020"
    filename_cov = basepath+"python_pandas/GGDCOVID19/"+"HPZonedata_" + yearstr + ".ftr"
    print("reading "+ filename_cov)
    df = pd.read_feather(filename_cov)
    df["datetimeobj"] = pd.to_datetime(df["TijdstiprapportageCOVID19besmetting"], errors = 'coerce')
    print(df.shape)
    yearstr = "2021"
    filename_cov = basepath+"python_pandas/GGDCOVID19/"+"HPZonedata_" + yearstr + ".ftr"
    print("reading "+ filename_cov)
    df2 = pd.read_feather(filename_cov)
    df2["datetimeobj"] = pd.to_datetime(df2["TijdstiprapportageCOVID19besmetting"], errors = 'coerce')
    df2["RINPERSOON"] = df2["Rinpersoon"]
    print(df2.shape)

    print("Concatenating, sorting, resetting index...")
    df = pd.concat([df,df2], ignore_index=True)
    df.sort_values(by=["RINPERSOON"], inplace=True)
    df.reset_index(inplace=True,drop=True)
        
    print(df.shape)
    print()

    df["keep"] = 0
    df["covidinf_year1nr"] = -1
    df["covidinf_year2nr"] = -1
    df["covidinf_year3nr"] = -1
    df["covidinf_year4nr"] = -1
    df["covidinf_week1nr"] = -1
    df["covidinf_week2nr"] = -1
    df["covidinf_week3nr"] = -1
    df["covidinf_week4nr"] = -1
    df["covidinf_date1"] = None
    df["covidinf_date2"] = None
    df["covidinf_date3"] = None
    df["covidinf_date4"] = None

    index_keep = -1
    rinp_str_prev = "NONE"
    rinp_str_selected = "START"

    total_nr_infections = 0
    index_keep = 0
    start = time.time()
    for index, rowdata in df.iterrows():
        if index % 100000 == 0:
            print(index)    
            print(time.time() - start)
            print(total_nr_infections)
            start = time.time()
            print()

        rinp_str = rowdata["RINPERSOON"]

        if rinp_str != rinp_str_prev:
            if rinp_str_prev == rinp_str_selected:               
                df.at[index_keep,"covidinf_week1nr"]=week1
                df.at[index_keep,"covidinf_week2nr"]=week2
                df.at[index_keep,"covidinf_week3nr"]=week3
                df.at[index_keep,"covidinf_week4nr"]=week4
                df.at[index_keep,"covidinf_year1nr"]=year1
                df.at[index_keep,"covidinf_year2nr"]=year2
                df.at[index_keep,"covidinf_year3nr"]=year3
                df.at[index_keep,"covidinf_year4nr"]=year4
                df.at[index_keep,"covidinf_date1nr"]=date1
                df.at[index_keep,"covidinf_date2nr"]=date2
                df.at[index_keep,"covidinf_date3nr"]=date3
                df.at[index_keep,"covidinf_date4nr"]=date4

            week1 = -1
            week2 = -1
            week3 = -1
            week4 = -1
            year1 = -1
            year2 = -1
            year3 = -1
            year4 = -1
            date1 = -1
            date2 = -1
            date3 = -1
            date4 = -1
            nr_pos = 0

        result = rowdata["TypeuitslagCOVID19test"]
        if not math.isnan(result):
            result = int(result)
            if result>=1 and result<=3: # positief
                nr_pos += 1
                this_date = rowdata["datetimeobj"]
                weeknr = this_date.isocalendar()[1]
                year = this_date.year
                month = this_date.month
                if month == 12 and (weeknr==1 or weeknr==53):
                    weeknr=52
                total_nr_infections+=1  

                if nr_pos==1:
                    week1= weeknr
                    year1= year
                    date1 = this_date     
                    df.at[index,"keep"]=1
                    index_keep = index                   
                elif nr_pos==2:
                    if weeknr != prev_weeknr or year!=prev_year:
                        week2= weeknr
                        year2= year
                        date2 = this_date  
                elif nr_pos==3:
                    if weeknr != prev_weeknr or year!=prev_year:
                        week3= weeknr
                        year3= year
                        date3 = this_date 
                else: # so all positive tests >= the fourth will be marked as the fourth!
                    if weeknr != prev_weeknr or year!=prev_year:
                        week4= weeknr
                        year4= year
                        date4 = this_date 

                prev_weeknr = weeknr
                prev_year = year
                rinp_str_selected = rinp_str
                
            rinp_str_prev = rinp_str
            #DEBUG
            # if index>100001:
            #     break
        
    print("Selecting only rows with data (keep)...")
    df = df[  df['keep']==1 ]
    df.reset_index(inplace=True,drop=True)
    print(df.shape)

    print("Selecting only relevant columns...")
    use_cols = ["RINPERSOON","covidinf_year1nr","covidinf_year2nr","covidinf_year3nr","covidinf_year4nr",
                "covidinf_week1nr","covidinf_week2nr","covidinf_week3nr","covidinf_week4nr",
                "covidinf_date1nr","covidinf_date2nr","covidinf_date3nr","covidinf_date4nr"]
    df = df[use_cols]
    print(df.shape)
    print()

    df["covidinf_date1nr"] = pd.to_datetime(df["covidinf_date1nr"], errors = 'coerce')
    df["covidinf_date2nr"] = pd.to_datetime(df["covidinf_date2nr"], errors = 'coerce')
    df["covidinf_date3nr"] = pd.to_datetime(df["covidinf_date3nr"], errors = 'coerce')
    df["covidinf_date4nr"] = pd.to_datetime(df["covidinf_date4nr"], errors = 'coerce')

    filename_core =  "GGDCOVID19_2020_2021_onerowpp" + versionstr
    # filename_core =  "vektPrest_HeartDiag_ext_myocardinfarct_onerowpp_" + yearstr+ versionstr

    filename_csv =  basepath_csv+filename_core+"_head.csv"
    print("writing (head): "+filename_csv)
    start = time.time()
    df.head(1000).to_csv(filename_csv)
    print(time.time() - start)

    filename_ftr = basepath_ftr +filename_core +".ftr"
    print("writing: "+filename_ftr)
    start = time.time()
    df.to_feather(filename_ftr)
    print(time.time() - start)

    
    
if __name__ == '__main__':
    run_main()
    