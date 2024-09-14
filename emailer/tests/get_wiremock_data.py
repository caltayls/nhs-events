import requests
import json
from bs4 import BeautifulSoup
import os


def login(session):
        # Get the authenticity token from the login page
        TFG_EMAIL="callumtaylor955@gmail.com"
        TFG_PW="aws_tick_pass"
        login_url = 'https://nhs.ticketsforgood.co.uk/users/sign_in'
        with session.get(login_url) as response:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
        form = soup.select_one("form.simple_form[action='/users/sign_in']")
        authenticity_token = form.select_one("input[name*='auth']")['value']
        login_data = {
            'authenticity_token': authenticity_token, # can't log in without token
            'user[email]': TFG_EMAIL,
            'user[password]': TFG_PW,
            'commit': 'Log in' # this posts the log in
        }
        headers = {
            'Referer': login_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Login to the webpage
        session.post(login_url, data=login_data, headers=headers)


site_info_path = "src/parse_events/site_info.json"
with open(site_info_path, "r") as file:
    info_all_sites = json.load(file)

for key in info_all_sites.keys():
  session = requests.Session()
  if key == "ticketsforgood":
      login(session)
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
