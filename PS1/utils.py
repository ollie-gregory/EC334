import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

def get_naics_descriptions(df):
    """
    Gets NAICS descriptions for a dataframe efficiently by only querying unique codes.
    
    Args:
        df: DataFrame containing a 'naics' column
        
    Returns:
        DataFrame with added 'naics_name' column
    """
    # Get unique NAICS codes
    unique_codes = df['naics'].unique()
    
    # Create a dictionary to store the results
    naics_dict = {}
    
    # Define headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    # Make single request to the website
    url = "https://www.naics.com/six-digit-naics/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML once
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all elements with class 'sixlink naicscode'
        code_elements = soup.find_all(class_='sixlink naicscode')
        
        # Create a dictionary of all NAICS codes and descriptions from the page
        for code_element in code_elements:
            anchor = code_element.find('a')
            if anchor:
                code = anchor.text.strip()
                title_div = code_element.find_next(class_='sixlink naicstit')
                if title_div and title_div.find('a'):
                    description = title_div.find('a').text.strip()
                    naics_dict[code] = description
        
        # Map descriptions to the dataframe
        df_copy = df.copy()
        df_copy['naics_name'] = df_copy['naics'].astype(str).map(naics_dict)
        
        return df_copy
        
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return df