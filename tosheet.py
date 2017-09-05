import urllib
import pprint
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import subprocess
import os
import time
import string
import sys


###ARGUMENTS:### 
# 1: CSV FILE to be Passed to Google Sheets
# 2: GoogleSheet Name, Spaces not working
# 3: SheetName, Optional, defaults to Sheet1
# 4: Additional Columns, Int, will not overwrite data
###

myfile=sys.argv[1]
myWorksheet = sys.argv[2]

extColNum=1

nargs = len(sys.argv)

#Remember, number of arguments is +1 from sys.argv
if nargs > 3:
    sheetname=sys.argv[3]
    if nargs > 4:
        extColNum=int(sys.argv[4])

#myfile="/home/bitnami/temp/coins.csv"
#myWorksheet = "Crypto Currencies"


print myfile
print myWorksheet

df = pd.read_csv(myfile)

# use creds to create a client to interact with the Google Drive API

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('/home/bitnami/auth/client_secret.json', scope)

client = gspread.authorize(creds)


def gsConnect(creds):
    global sheet
    global client
    client = gspread.authorize(creds)
    if nargs == 3:
        sheet = client.open(myWorksheet).sheet1
    if nargs > 3:
        sheet = client.open(myWorksheet).worksheet(sheetname)
    return sheet


def insRange(myDF,mySheet):
    clet=string.ascii_uppercase[len(myDF.columns.values)-1]
    cell_list=mySheet.range('A1:'+clet + str(len(myDF.index)+1) )
    nc = len(myDF.columns.values)
    n=0
    h=0
    for cell in cell_list:
        if h<nc:
            cell.value = myDF.columns.values[h]
            h+=1
        else:
            cell.value = myDF.values.flatten().tolist()[n]
            n+=1
    mySheet.update_cells(cell_list)


gsConnect(creds)

#sheet = client.open(myWorksheet).worksheet(d)

rows = len(df)+1
cols = len(df.columns.values)+extColNum

sheet.resize(rows,cols)

insRange(df,sheet)


