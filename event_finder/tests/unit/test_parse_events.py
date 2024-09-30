import time
import pytest
import json
import bs4
import pandas as pd
from unittest.mock import AsyncMock
from aiohttp import ClientSession
from src.parse_events import EventParser


@pytest.fixture
def mock_site_info():
    with open(r"event_finder/tests/resources/site_info.json", 'r') as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_parse_event_cards(mocker, mock_site_info):
    # Arrange
    website = 'ticketsforgood'
    # Mock init json loader
    mock_open = mocker.mock_open(read_data=json.dumps(mock_site_info))
    mocker.patch("src.parse_events.open", mock_open)
    mocker.patch("src.parse_events.json.load", return_value=mock_site_info)
    
    scraper = EventParser(website)
    url = 'http://localhost:8080/ticketsforgood'

    # mock sem
    sem = AsyncMock()

    # Act
    # Test the async method
    async with ClientSession() as session:
        result = await scraper.parse_event_cards(session, sem, url)
    
    # Assert
    assert len(result) == 12
    assert "3\">\nBongo's Bingo\n</h5>\n<d" in str(result[11])
    assert " mb-3\">\nShrek The Musical (Discounted Off" in str(result[9])



def test_parse_card_info():
    
    # Setup
    websites = ['concertsforcarers', 'bluelighttickets', 'ticketsforgood']

    for website in websites:

        with open(f"event_finder/tests/resources/test_{website}_card_html.json", 'r') as f:
            card_dict = json.load(f)
        
        cards = [bs4.BeautifulSoup(card, 'html.parser') for card in card_dict.values()]
        
        # Act
        ep = EventParser(website)
        results = {i: ep.parse_card_info(card) for i, card in enumerate(cards)}
        with open(f"event_finder/tests/resources/test_{website}_cards_parsed.json", 'w') as f:
            card_dict = json.dump(results, f)
        
        # Assert
        actual = {
            'ticketsforgood': {
                'card3': {
                    "event_name": "York Knights & Valkyrie 2024 Home Games (Discounted Offer)",
                    "event_type": "Sport",
                    "location": "LNER Community Stadium, York",
                    "date": "19 May\n-\n29 September",
                    "url": "/events/215784-york-knights-valkyrie-2024-home-games-discounted-offer"
                },
                'length': 12
            },
            'bluelighttickets': {
                'card3': {
                    "event_name": "Big Saturday Night Show",
                    "location": "Dundee,",
                    "date": "31st Aug 2024",
                    "url": "/event/6696"
                },
                'length': 9
            },
            'concertsforcarers': {
                'card3': {
                    "event_name": "Hot Wheels\u00e2\u0084\u00a2 City Experience (Add a total of 8 Tickets to the ballot!) - Hot Wheels\u00e2\u0084\u00a2 City Experience",
                    "location": "B.E.C Arena, Manchester",
                    "date": "September 5, 2024",
                    "url": "/events/hot-wheels-city-experience-add-a-total-of-8-tickets-to-the-ballot-4688-bec-arena-manchester-sep-5-2024"
                },
                'length': 11
            }
        }

        assert results.get(3) == actual[website]['card3']
        assert len(results) == actual[website]['length']


def test_html_to_dataframe(mocker):
    # Setup

    websites = ['ticketsforgood']

    for website in websites:

        with open(f"event_finder/tests/resources/test_{website}_cards_parsed.json", 'r') as f:
            card_dict = json.load(f)

        mock_parse_card_info = mocker.Mock()
        mock_parse_card_info.side_effect = card_dict.values()
        mocker.patch("src.parse_events.EventParser.parse_card_info", mock_parse_card_info)
        
        # Act
        ep = EventParser(website)
        result = ep.html_to_dataframe(range(len(card_dict)))

    # Assert
    df_row1 = {
        "event_name": "The Gin To My Tonic Show: The Ultimate Gin & Spirit Festival (Discounted Offer)",
        "event_type": "Festivals",
        "location": "Various Venues, UK, UK",
        "date": "17 November-21 September",
        "url": "/events/135494-the-gin-to-my-tonic-show-the-ultimate-gin-spirit-festival-discounted-offer",
        "website": "https://nhs.ticketsforgood.co.uk"
    }
    assert len(result) == 12
    result.loc[0].to_json(orient="records") == df_row1


def test_reformat_df():
    # Setup
    websites = ['concertsforcarers', 'bluelighttickets', 'ticketsforgood']
    dfs = []
    for website in websites:
        dfs.append(pd.read_json(f"event_finder/tests/resources/test_{website}_df_results.json", orient='records', convert_dates=False))

    # Act
    result = EventParser.reformat_df(dfs)
    
    # Assert
    formatted_df_idx7 = {
        "index": 7,
        "event_name": "Cafe Mambo Ibiza Classics On The Beach",
        "location": "Weston Super Mare Beach in Weston Super-Mare",
        "date": "September 7, 2024",
        "url": "https://www.concertsforcarers.org.uk/events/cafe-mambo-ibiza-classics-on-the-beach-4643-weston-super-mare-beach-in-weston-super-mare-sep-7-2024",
        "website": "https://www.concertsforcarers.org.uk",
        "event_type": None,
        "website_name": "concertsforcarers",
        "date_end": "2024-09-07T00:00:00.000"
    }

    row8 = result.loc[7]
    assert row8['event_name'] == formatted_df_idx7['event_name']
    assert row8['location'] == formatted_df_idx7['location']
    assert row8['url'] == formatted_df_idx7['url']
    assert row8['date_end'] == pd.to_datetime(formatted_df_idx7['date_end'])
    assert row8['website_name'] == formatted_df_idx7['website_name']


@pytest.mark.asyncio
async def test_fetch_html(mocker, mock_site_info):

    # Setup
    websites = ['concertsforcarers', 'bluelighttickets', 'ticketsforgood']

    for website in websites:
        # Mock init json loader
        mock_open = mocker.mock_open(read_data=json.dumps(mock_site_info))
        mocker.patch("src.parse_events.open", mock_open)
        mocker.patch("src.parse_events.json.load", return_value=mock_site_info)
        mocker.patch("src.parse_events.EventParser.login")
        
        parser = EventParser(website)
            
        # Act
        result = await parser.fetch_html()

        # Assert
        actual = {
            'ticketsforgood': "Hayward Gallery - Tavares Strachan: There Is Light Somewhere (Disc",
            'bluelighttickets': "Midweek Racing - Goodwood Racecourse</span>\n</figure>\n</a>\n</h3>",
            'concertsforcarers': "class=\"event__title\" itemprop=\"name\"><span>The Gin To My Tonic Festival (70% Discount on Tickets) Evening Session</span></di"
        }

        assert actual[website] in str(result[8])

 



    

