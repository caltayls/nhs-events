import pytest
import json
from functools import lru_cache
import pandas as pd
from datetime import datetime, date
from emailer.src.utils import get_areas_from_county
from emailer.src import build_email_content

users = {
    "Items": [
        {
            'uuid': 'uuid1',
            'freq': 'hourly',
            'email': 'email1@email',
            'locations': ['Berkshire', 'Derbyshire']
        },
        {
            'uuid': 'uuid2',
            'freq': 'hourly',
            'email': 'email2@email',
            'locations': ['Leicestershire', 'Cambridgeshire']
        },
        {
            'uuid': 'uuid3',
            'freq': 'daily',
            'email': 'email3@email',
            'locations': ['All']
        },
        {
            'uuid': 'uuid4',
            'freq': 'weekly',
            'email': 'email4@email',
            'locations': ['Tyne & Wear', 'Greater Manchester']
        }
    ]
}

@pytest.fixture
def mock_datetime(mocker):
    def _mock_datetime(hour, date):
        mock_dt = mocker.Mock()
        mock_dt.hour = hour
        mock_dt.isocalendar.return_value = [2024, 41, 5]
        mock_dt.date.return_value = date

        mock_datetime = mocker.patch("emailer.src.build_email_content.datetime")
        mock_datetime.today.return_value = mock_dt
    return _mock_datetime


@lru_cache(maxsize=1)
def get_dfs() -> dict[pd.DataFrame]:
    events_df = pd.read_json('event_finder/tests/resources/test_df_reformatted.json', orient='records')
    user_df = pd.DataFrame(users['Items'])
    location_df = pd.read_csv('event-location-getter/locations.csv')
    return {
        'events': events_df,
        'users': user_df,
        'locations': location_df
    }


def test_get_events_based_on_freq_hourly(mocker, mock_datetime):
    # Setup
    dfs = get_dfs()
    events_df, user_df = dfs["events"], dfs["users"]

    mock_datetime(17, date(2024, 10, 11))
    # Hourly user
    user = user_df.iloc[0]

    # Act
    actual = build_email_content.get_events_based_on_freq(user, events_df)

    # Assert
    assert len(actual) == 3
    assert len(actual["created_at"].dt.hour == 17) == 3


def test_get_events_based_on_freq_daily(mocker, mock_datetime):   
    # Setup
    dfs = get_dfs()
    events_df, user_df = dfs["events"], dfs["users"]

    mock_datetime(17, date(2024, 10, 11))
    # daily user
    user = user_df.iloc[2]

    # Act
    actual = build_email_content.get_events_based_on_freq(user, events_df)

    # Assert
    assert len(actual) == 8
    assert len(actual["created_at"].dt.day == 11) == 8
    

def test_get_events_based_on_freq_weekly(mocker, mock_datetime):      
    # Setup
    dfs = get_dfs()
    events_df, user_df = dfs["events"], dfs["users"]

    mock_datetime(17, date(2024, 10, 11))
    # weekly user
    user = user_df.iloc[3]

    # Act
    actual = build_email_content.get_events_based_on_freq(user, events_df)

    # Assert
    assert len(actual) == 31
    assert len(actual["created_at"].dt.isocalendar()['week'] == 41) == 31
    


    


    
