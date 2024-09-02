import pandas as pd
import requests
from io import StringIO

import streamlit as st

# Replace this with your Google Sheet ID
sheet_id = st.secrets["sheet_id"]

# URL to fetch the CSV export of the Google Sheet
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Use requests to get the CSV data
response = requests.get(url)

# Raise an error if the request was unsuccessful
response.raise_for_status()


# Convert the CSV data to a pandas DataFrame
df = pd.read_csv(StringIO(response.text), sep=",", index_col=False)

# Display the DataFrame
# print(df.head())

df.replace({r'[^\x00-\x7F\u00A3]+':''}, regex=True, inplace=True)

df = df.drop(columns=['Item number', 'Payout AD', 'Payout NS', 'Payout JP', 'Payout MP', 'Due to NS', 'Due to JP', 'Due to MP'])

password = st.text_input("Password", type="password")

df = df[df['Password'] ==  password]

df = df.drop(columns=['Email', 'Password'])

st.dataframe(df.head(), height=750, hide_index=True)