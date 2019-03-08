import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
from pathlib import Path

"""Sheety To Spreadsheet Script
Developed for Bubbleye

Can be run either as a script with variables passed or directly import 'insert_df()' in Python.

Arguments:
    my_file_path: path of file to be sent to GS
    spreadsheet_name: Name of Main Spreadsheet
    sheet_name: Name of worksheet (tab name)
    additional empty columns, int: (optional) can be extra columns, will preserve data

from python:
    from sheety.tosheet import insert_df
    insert_df(df, spreadsheet_name, sheet_name, additional_cols)

from R:
    system(paste(PY_EXECUTABLE, TO_SHEET_SCRIPT, my_file_path, spreadsheet_name, worksheet_name, additional_cols))
"""

def clean(my_df):
    my_df.replace([np.inf, -np.inf], 'inf', inplace = True)
    my_df.replace([np.nan], 'nan', inplace = True)
    return(my_df)


def ensure_sheetname(client, my_spreadsheet, sheetname):
    result = client.open(my_spreadsheet).worksheets()
    sn = []
    for r in result:
        sn.append(r.title)
    if sheetname not in sn:
        client.open(my_spreadsheet).add_worksheet(sheetname, rows = 1, cols = 1)


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def insert_range(my_df, target_sheet):
    clet = colnum_string(len(my_df.columns.values))
    cell_list = target_sheet.range('A1:'+ clet + str(len(my_df.index) + 1))
    nc = len(my_df.columns.values)
    n = 0
    h = 0
    for cell in cell_list:
        if h < nc:
            cell.value = my_df.columns.values[h]
            h += 1
        else:
            cell.value = my_df.values.flatten().tolist()[n]
            n += 1
    target_sheet.update_cells(cell_list)


def insert_df(df, dest_spreadsheet, dest_sheetname, extra_cols):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    df = clean(df)
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_path, scope)
    client = gspread.authorize(creds)
    ensure_sheetname(client, dest_spreadsheet, dest_sheetname)
    sheet = client.open(dest_spreadsheet).worksheet(dest_sheetname)
    rows = len(df) + 1
    cols = len(df.columns.values) + extra_cols
    sheet.resize(rows, cols)
    insert_range(df, sheet)


home = str(Path.home())
client_secret_path = home +'/sheety/sheety-credentials.json'


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    client_secret_path = "{0}/{1}".format(dir_path, 'sheety-credentials.json')
    nargs = len(sys.argv)
    my_file_path = sys.argv[1]
    my_spreadsheet = sys.argv[2]
    sheet_name = sys.argv[3]
    df = pd.read_csv(my_file_path)
    if nargs > 4:
        extra_cols = int(sys.argv[4])
    else:
        extra_cols = 0
    df = df.fillna('nan')
    insert_df(df, my_spreadsheet, sheet_name, extra_cols)

