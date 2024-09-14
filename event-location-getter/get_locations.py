import requests
from bs4 import BeautifulSoup
import pandas as pd

url = r"https://en.wikipedia.org/wiki/List_of_ONS_built-up_areas_in_England_by_population"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")
table_html = {
  "cities": tables[1],
  "large_towns": tables[2],
  "med_towns": tables[3],
  "small_towns": tables[4],
  "smaller_towns": tables[5]
}

df_list =[]
for html in table_html.values():
  df = pd.read_html(str(html), index_col=0)[0]
  if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(0)
  df = df.rename(columns={"BUA": "Built-up area"}, errors="ignore")
  df_list.append(df)

df_list.__len__()
for df in df_list:
  print(df.columns)
master_df = pd.concat(df_list, ignore_index=True)

master_df = master_df[["Built-up area", "County"]]
master_df = master_df.sort_values(by="County")
master_df.to_csv("locations.csv", index=False)
len(master_df["County"].unique())
