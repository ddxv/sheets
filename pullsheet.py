import urllib
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import sys


###ARGUMENTS:### 
#myWorksheet = "Crypto Currencies"
#sheetname="CashFlow"

#print myfile
#print myWorksheet

def sheet_df(myWorksheet,sheetname):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/bitnami/auth/client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(myWorksheet).worksheet(sheetname)
    listDF=sheet.get_all_values()
    myHeaders=listDF[0]
    df=pd.DataFrame(listDF[1:],columns=myHeaders)
    return(df)

if __name__ == "__main__":
    sheet_df(sys.argv[1], sys.argv[2])


