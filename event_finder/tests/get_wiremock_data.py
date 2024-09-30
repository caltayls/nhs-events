import requests
import json
from bs4 import BeautifulSoup
import os




site_info_path = "src/parse_events/site_info.json"
with open(site_info_path, "r") as file:
    info_all_sites = json.load(file)

for key in info_all_sites.keys():
  session = requests.Session()
  page_url =  info_all_sites[key]['URL_BASE'] + info_all_sites[key]['FIRST_PAGE_REL_PATH']
  response = session.get(page_url)
  content = response.text

  stub_map = {
    "request": {
        "method": "GET",
        "url": page_url
    },
    "response": {
        "status": response.status_code,
        "body": content,
        "headers": {
        "Content-Type": response.headers.get('Content-Type', 'text/html')
        }
    }
  }
  mappings_dir = "wiremock/mappings"
  filename = f'{key}-mapping.json'
  filepath = os.path.join(mappings_dir, filename)

  # Write the mapping to a JSON file
  with open(filepath, 'w') as f:
    json.dump(stub_map, f, indent=4)
