import pandas as pd
import requests
from io import StringIO

import streamlit as st


st.set_page_config(
    page_title="Dentons of Dudley",
)


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
df.drop(df.tail(1).index,inplace=True)
df = df[df['Item number'].notna()]


df = df.rename(columns=lambda x: x.strip())


df.replace({r'[^\x00-\x7F\u00A3]+':''}, regex=True, inplace=True)

df = df.drop(columns=['Item number', 'Payout AD', 'Payout NS', 'Payout JP', 'Payout MP', 'Due to NS', 'Due to JP', 'Due to MP'], axis=1)

st.title("Dentons of Dudley")


password = st.text_input("Password", type="password")

df = df[df['Password'] == password]

df = df.drop(columns=['Password'])

st.dataframe(df, height=750, hide_index=True)