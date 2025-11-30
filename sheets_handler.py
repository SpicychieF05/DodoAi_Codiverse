import os
import json
import base64
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

class GoogleSheetsManager:
    def __init__(self):
        self.credentials_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        self.spreadsheet_id = os.getenv("LEADS_SHEETS_SPREADSHEET_ID")
        self.sheet_name = os.getenv("LEADS_SHEETS_RANGE", "Sheet1")
        self.client = None
        self.sheet = None
        self.connect()

    def connect(self):
        try:
            if not self.credentials_json:
                raise ValueError("GOOGLE_SHEETS_CREDENTIALS not found in .env")
            
            # Decode base64 credentials
            creds_dict = json.loads(base64.b64decode(self.credentials_json))
            
            credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            self.client = gspread.authorize(credentials)
            
            # Open the spreadsheet and specific worksheet
            spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            try:
                self.sheet = spreadsheet.worksheet(self.sheet_name)
                print(f"Successfully connected to Google Sheet: {self.sheet_name}")
            except gspread.WorksheetNotFound:
                print(f"Worksheet '{self.sheet_name}' not found. Creating it...")
                self.sheet = spreadsheet.add_worksheet(title=self.sheet_name, rows=1000, cols=10)
                # Add headers
                self.sheet.append_row(["CMID", "Name", "Service", "Details", "Status", "Timestamp"])
                print(f"Created new worksheet: {self.sheet_name}")
                
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            raise

    def add_lead(self, cmid: str, name: str, service: str, details: str) -> bool:
        try:
            # Append row: [CMID, Name, Service, Details, Status, Timestamp]
            # Status defaults to "Pending"
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row = [cmid, name, service, details, "Pending", timestamp]
            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error adding lead: {e}")
            return False

    def get_status(self, cmid: str) -> dict:
        try:
            # Search for the CMID in the first column
            cell = self.sheet.find(cmid)
            if cell:
                row_values = self.sheet.row_values(cell.row)
                # Assuming structure: [CMID, Name, Service, Details, Status, Timestamp]
                return {
                    "cmid": row_values[0],
                    "name": row_values[1],
                    "service": row_values[2],
                    "details": row_values[3],
                    "status": row_values[4],
                    "timestamp": row_values[5]
                }
            return None
        except gspread.exceptions.CellNotFound:
            return None
        except Exception as e:
            print(f"Error getting status: {e}")
            return None
