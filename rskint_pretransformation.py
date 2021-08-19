#IMPORTING MODULES
import csv
import sys
import math
import pandas as pd
import time
from datetime import datetime,timedelta

time = str((int(time.time())))
intput_filename='C:/Users/patelsm/Desktop/git_implementation/ifrs17_scripts/data/JUNE01/RSKINT.DAT'
final_filename='C:/Users/patelsm/Desktop/git_implementation/ifrs17_scripts/data/JUNE01/MAPPED_RSKINT.datCDNDI20210530191750'
control_filename='C:/Users/patelsm/Desktop/git_implementation/ifrs17_scripts/data/JUNE01/RSKINT.CTL'

#INPUT TO DATAFRAME
inputreader = pd.read_csv(intput_filename, delimiter = ',',na_filter=False,low_memory=False)


#WRITE TO CSV
def writer(df):        
        df.to_csv(final_filename,index=False,mode='a',quoting=csv.QUOTE_ALL,header=False)

#CREATE CONTROL FILE
def cntrlfile(df_ctr):
        f = open(control_filename,'w')
        f.write(df_ctr)
        f.close()

#GET LAST DAY OF THE QUARTER
def getEOQdate(accounting_date):         
        current_quarter = math.floor((accounting_date.month - 1) / 3 + 1)
        current_quarter_lastday = datetime(accounting_date.year, 3 * current_quarter + 1, 1) + timedelta(days=-1)
        return current_quarter_lastday

#READ AND WRITE ROWS
def main():
    count=0
    dr_amount=0
    cr_amount=0                        
    df2=pd.DataFrame()

    inputreader.loc[(inputreader['Calculation Step']=='OPENING_CURRENT'),'Accounting Date']=inputreader.loc[(inputreader['Calculation Step']=='OPENING_CURRENT'),'Accounting Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d').date()-timedelta(1))
    inputreader.loc[(inputreader['Calculation Step'].isin(['OPENING_INCEPTION','LIC_OPENING_CURRENT','PAA_OPENING'])),'Accounting Date']=inputreader.loc[(inputreader['Calculation Step']=='OPENING_INCEPTION'),'Accounting Date'].apply(lambda x: getEOQdate(datetime.strptime(x,'%Y-%m-%d').date()).strftime('%Y-%m-%d'))
    inputreader.loc[~(inputreader['Calculation Step'].isin(['OPENING_CURRENT','OPENING_INCEPTION'])),'Accounting Date']=inputreader.loc[~(inputreader['Calculation Step'].isin(['OPENING_CURRENT','OPENING_INCEPTION'])),'Reporting Date']
    inputreader.loc[(inputreader['Amount in Transaction Currency']!=0)&(inputreader['Valuation Method'].isin(['GMM','VFA'])),'Amount in Transaction Currency']=inputreader.loc[(inputreader['Amount in Transaction Currency']!=0)&(inputreader['Valuation Method'].isin(['GMM','VFA'])),'Amount in Transaction Currency'].apply(lambda x: round(x, 2))
    

    dr_amount = inputreader.loc[inputreader["Debit / Credit"] == "DR", "Amount in Transaction Currency"].sum()
    cr_amount = inputreader.loc[inputreader["Debit / Credit"] == "CR", "Amount in Transaction Currency"].sum()

    
    column_names=["Hierarchy Node","Line No.","Date","Accounting Date","Portfolio","IFRS 17 Group","Group Type","Valuation Method",
    "Modified GMM","Calculation Step","Accounting Policy","Onerosity at Opening","Onerosity at New Business",
    "Onerosity at the Start of the Analysis","Onerosity at the End of the Analysis","Variable","Definition of Variable",
    "Account Code","Account Name","Transaction Currency","Amount in Transaction Currency","Functional Currency","Amount in Functional Currency",
    "Debit / Credit","Underlying IFRS 17 Group","Insurance Product","Reinsurance Held","Country","Reinsurance Type","Insurance Contract Type at Opening",
    "Insurance Contract Type at Closing","Transaction Number","Code of Posting Rule","Code of Master Account","Macro Section of Master Account",
    "Valuation Method of Master Account","Insurance Type of Master Account","LRC/LIC of Master Account","Section Header of Master Account",
    "Subsection of Master Account","Movement Analysis Flow of Master Account","","cohort_code","currency_code","dividend_class","division",
    "elim_company_cd","gl_legal_id","gl_portfolio_code","gl_reinsurance_class_code","ira_calculation","lob_cd","new_business_type",
    "onerous_indicator","reporting_currency_code","treaty_code"]
    
    df2 = inputreader.reindex(columns=column_names) 
    df2=df2[round(df2["Amount in Transaction Currency"],2)!=0&(df2['Valuation Method'].isin(['GMM','VFA']))]   
    

    df_ctl = "Records: "+str(len(df2.index))+" Debits: "+str(round(dr_amount,2))+" Credits: "+str(round(cr_amount,2))
    
    cntrlfile(df_ctl)
    writer(df2) 


main()