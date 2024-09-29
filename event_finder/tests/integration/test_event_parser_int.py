import pytest
import json
import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from src.parse_events import EventParser

with open("event_finder/src/site_info.json", 'r') as f:
    website_html_elements = json.load(f)


@pytest.mark.asyncio
async def test_tfg_login():
    # Act
    ep = EventParser('ticketsforgood')
    async with ClientSession() as session:
        result = await ep.login(session)
        resp_text = await result.text()

    # Assert
    unsuccessuful_html = "Login to Tickets for Good"
    assert unsuccessuful_html not in resp_text
    assert result.status == 200


def test_tfg_html_elements():
    html_dict = website_html_elements['ticketsforgood']
    url = r"https://nhs.ticketsforgood.co.uk/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Check event card html
    event_cards = soup.select(html_dict['EVENT_CARD_SEL'])
    assert len(event_cards) != 0

    # final page element
    final_page_element = soup.select(html_dict['LAST_PAGE_ELEMENT_SEL'])[-1]['href']
    assert final_page_element

def test_blt_html_elements():
    html_dict = website_html_elements['bluelighttickets']
    url = r"https://bluelighttickets.co.uk/event/all"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Check event card html
    event_cards = soup.select(html_dict['EVENT_CARD_SEL'])
    assert len(event_cards) != 0

    # final page element
    final_page_element = soup.select(html_dict['LAST_PAGE_ELEMENT_SEL'])[-1]['href']
    assert final_page_element

def test_cfc_html_elements():
    html_dict = website_html_elements['concertsforcarers']
    url = r"https://www.concertsforcarers.org.uk/events"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Check event card html
    event_cards = soup.select(html_dict['EVENT_CARD_SEL'])
    assert len(event_cards) != 0



