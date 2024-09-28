import urllib3
import pytest
import json

from src.parse_events import EventParser


@pytest.fixture
def mock_site_info():
    with open("tests/site_info.json", 'r') as f:
        return json.load(f)


@pytest.fixture
def event_parser():
    return {
        'tfg': EventParser("ticketsforgood"),
        'blt': EventParser("bluelighttickets"),
        'cfc': EventParser("concertsforcarers")
    }


@pytest.mark.asyncio
async def test_parse_event_cards(mocker, mock_site_info):
    # Mock website information
    website = 'ticketsforgood'
    site_info = mock_site_info[website]

    # Create an instance of EventParser
    scraper = EventParser(website)
    scraper.site_info = site_info 

    # Mock HTML content that the page might return
    http = urllib3.PoolManager()
    url = 'http://localhost:8080/ticketsforgood'  # Replace with your actual WireMock URL
    response = http.request('GET', url)
    mock_html_content = response.data.decode('utf-8')


    # Mock the response for session.get()
    mock_response = mocker.AsyncMock()
    mock_response.text = mocker.AsyncMock(return_value=mock_html_content)

    # Mock the session object
    mock_session = mocker.AsyncMock()
    mock_session.get = mocker.AsyncMock(return_value=mock_response)

    # Mock the semaphore to ensure it's used correctly
    mock_sem = mocker.AsyncMock()

    # Mock asyncio.sleep to avoid unnecessary delays during tests
    mocker.patch('asyncio.sleep', return_value=None)


    result = await scraper.parse_event_cards(mock_session, mock_sem, url)
    print(result)

    # Assert that session.get() was called with the correct URL
    mock_session.get.assert_called_once_with(url)

    # Assert semaphore was used correctly
    mock_sem.__aenter__.assert_called_once()

    # Verify that the event cards were parsed correctly from the mock HTML
    assert len(result) == 2
    assert result[0].text == 'Event 1'
    assert result[1].text == 'Event 2'



# @pytest.mark.asyncio
# async def test_fetch_html(mocker, event_parser, mock_site_info):
#     mock_login = mocker.patch.object(
#         event_parser['tfg'], 'login',
#         mocker.AsyncMock()
#     )  
#     mocker.patch(
#         "builtins.open",
#         mocker.mock_open(read_data=json.dumps(mock_site_info))
#     )
#     mocker.patch("json.load", return_value=mock_site_info)
#     event_parser['tfg'].fetch_html()

