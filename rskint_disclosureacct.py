#IMPORTING MODULES
import csv
import pandas as pd
import sys

#NAMING HEADERS
header_list = []
for i in range(1,87):
    header_list.append(i)

#INPUT TO DATAFRAME
inputreader = pd.read_csv('C:/Users/patelsm/Desktop/git_implementation/ifrs17_scripts/RSKINT.MAPPED', delimiter = ',',na_filter=False,names=header_list,dtype=str)

#DISCLOSURE ACCT LOOPUP DICT
data = pd.read_csv('C:/Users/patelsm/Desktop/git_implementation/ifrs17_scripts/Disclosure_Account_Mapping.csv',names=["old_acct", 0, 1])
data_acct= data.set_index('old_acct').T.to_dict()

#READ AND WRITE ROWS
def main():   
    for fields in inputreader.itertuples(index=False):                  
        df_before = pd.DataFrame(fields)              
        writer(df_before)
        acctlookup(df_before)

#PROCESS EACH LINE, ADD NEW LINE IF ACCT MATCH OR RETURN ORIGNAL
def acctlookup(df_before):     
      for i in df_before:            
            acct_map=data_acct.get(int(df_before.iat[85,0]),False)            
            if acct_map != False:
                for j in range(2):
                    if j == 0:                      
                        newacct1 = acct_map[j][0:7] +  df_before.iat[6,0][7] + acct_map[j][8:12]
                        df_before.iat[6,0] = newacct1                       
                        df_before.iat[11,0] = "IFRS17 Disclosure-"+df_before.iat[11,0]
                        writer(df_before)
                    else:
                        newacct2 = acct_map[j][0:7] +  df_before.iat[6,0][7] + acct_map[j][8:12]
                        df_before.iat[6,0] = newacct2                        
                        df_before.iat[11,0] = ""+df_before.iat[11,0]                    
                        df_before.iat[14,0] = float(df_before.iat[14,0])*-1
                        writer(df_before)       
#WRITE TO CSV
def writer(df):        
        df.T.to_csv('C:/Users/patelsm/Desktop/git_implementation/ifrs17_scripts/RSKINT_NEW.MAPPED',index=False,mode='a',quoting=csv.QUOTE_ALL, header=False)

main()