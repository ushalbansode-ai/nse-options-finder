"""NSE Bhavcopy Data Fetcher"""
import requests
from datetime import datetime, timedelta
import zipfile
import io
import pandas as pd
from pathlib import Path

class NSEBhavcopyFetcher:
    BASE_URL = "https://nsearchives.nseindia.com/content/historical/DERIVATIVES"
    
    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_bhavcopy(self, date=None):
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%d%b%Y").upper()
        date_path = date.strftime("%Y/%b")
        fo_url = f"{self.BASE_URL}/{date_path}/fo{date_str}bhav.csv.zip"
        
        try:
            response = requests.get(fo_url, timeout=30)
            response.raise_for_status()
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                csv_name = z.namelist()[0]
                df = pd.read_csv(z.open(csv_name))
                output_file = self.data_dir / f"fo_{date.strftime('%Y%m%d')}.csv"
                df.to_csv(output_file, index=False)
                return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
