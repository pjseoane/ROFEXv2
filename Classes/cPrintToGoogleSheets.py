# Imports for google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class cGoogleSetup():
    def __init__(self, jasonKeyFile, googleSheet):

        self.jasonKeyFile = jasonKeyFile
        self.googleSheet = googleSheet

        self.environment()

    def environment(self):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.jasonKeyFile, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(self.googleSheet).sheet1


class cPrintToGSheets():
    # TODO: armar esto para escribir un rango o un array
    def __init__(self, sheet, fila,columna,valueToWrite):
        self.sheet=sheet
        self.fila=fila
        self.columna=columna
        self.valueToWrite=valueToWrite

        self.sheet.update_cell(self.fila, self.columna, self.valueToWrite)
        #self.sheet.insert_row("ww",1)

class cPrintRangeToGSheets():
    def __init__(self, sheet, fila, columna, rangeToWrite):
        self.sheet = sheet
        self.fila = fila
        self.columna = columna
        self.rangeToWrite = rangeToWrite

        self.sheet.update_cells(self.fila, self.columna,self.rangeToWrite)