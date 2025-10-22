""" 
Scrape the Sumer Sports teams offensive and defensive stats pages to get data from 2022 to this season.

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Convert string columns to appropriate numeric types"""
    # Common numeric columns
    numeric_patterns = ['EPA', 'Rate', 'Plays', 'Rank', 'Pass', 'Rush', 
                        'Usage', 'Avg', 'Pct', 'Percentage', '%']
    
    for col in df.columns:
        if any(pattern in col for pattern in numeric_patterns):
            try:
                # Remove % signs and convert
                df[col] = df[col].str.replace('%', '').str.replace(',', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except (AttributeError, ValueError):
                continue
    
    return df

def scrape_sumer(o_or_d = "offensive", season=2025, refinement=None):
    url = f'https://sumersports.com/teams/{o_or_d}/'
    if refinement:
        url += f"/?refinement={refinement}"
    if season != 2025 and refinement:
        url += f'&season={season}'
    elif season != 2025 and not refinement:
        url += f'?season={season}'
    
    print(f"url: {url}")

    # Use this header to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table - adjust selector based on actual HTML structure
        table = soup.find('table')
        
        if not table:
            print("No table found. The page might require authentication or use JavaScript.")
            return None
        
        # Extract headers
        headers = []
        header_row = table.find('thead').find('tr') if table.find('thead') else table.find('tr')
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.text.strip())
        
        # Extract rows
        rows = []
        tbody = table.find('tbody') if table.find('tbody') else table
        for tr in tbody.find_all('tr'): # tr is table row
            row = []
            for td in tr.find_all(['td']):
                # print(f"text from td in a tr: {td.text.strip()}")
                row.append(td.text.strip())
            if row:  # Only add non-empty rows
                rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        df["Team"] = df["Team"].apply(lambda x: x.split(".")[1])
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None
    return df
    

if __name__ == "__main__":
    o_or_d = "offensive"
    refinement = None
    for season in [2025, 2024, 2023, 2022]:
        offensive_overview_data = scrape_sumer(o_or_d, season, refinement)
        offensive_overview_data = clean_dataframe(offensive_overview_data)
        if refinement:
            offensive_overview_data.to_csv(f'csvs/{refinement}_{o_or_d}_overview_{season}.csv', index=False)
        else:
            offensive_overview_data.to_csv(f'csvs/{o_or_d}_overview_{season}.csv', index=False)
