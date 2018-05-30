import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
from pathlib import Path

"""Sheety From Sheet Script
Developed for Bubbleye

Arguments:
    spreadsheet_name: Name of Main Spreadsheet
    sheet_name: Name of worksheet (tab name)
    dest_path_csv: (optional) path for csv file

    Note: If called without dest_path_csv, pull_worksheet() returns a Pandas DataFrame

from python:
    from sheety.pullsheet import pull_worksheet
    pull_worksheet(spreadsheet_name, sheet_name, dest_path_csv)

from R:
    system(paste(PY_EXECUTABLE, FROM_SHEET_SCRIPT, spreadsheet_name, worksheet_name, destination_path))

    Note: for R, destination_path is required, outputs a CSV
"""


def pull_worksheet(my_spreadsheet, sheetname, dest_csv):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(my_spreadsheet).worksheet(sheetname)
    listed_data = sheet.get_all_values()
    my_headers = listed_data[0]
    df = pd.DataFrame(listed_data[1:], columns = my_headers)
    if dest_csv is not None:
        df.to_csv(dest_csv, index = False, header = True)
    else:
        return(df)

home = str(Path.home())
client_secret_path = home +'/auth/sheety-credentials.json'

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    client_secret_path = "{0}/{1}".format(dir_path, 'sheety-credentials.json')
    if (len(sys.argv) == 3):
        pull_worksheet(sys.argv[1], sys.argv[2], None)
    if (len(sys.argv) == 4):
        pull_worksheet(sys.argv[1], sys.argv[2], sys.argv[3])


