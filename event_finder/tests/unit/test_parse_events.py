import pytest
import pytest_asyncio
import asyncio
import json


from src.parse_events import EventParser

@pytest.fixture
def mock_site_info():
  with open("tests/site_info.json", 'r') as f:
    return json.load(f)

@pytest.fixture
def event_parser():
  return EventParser("ticketsforgood")


@pytest.mark.asyncio
def test_fetch_html(mocker, event_parser, mock_site_info):

  mock_login = mocker.patch.object(event_parser, 'login', mocker.AsyncMock())  
  mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(mock_site_info)))
  mocker.patch("json.load", return_value=mock_site_info)
