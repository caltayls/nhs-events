import pytest
import pandas as pd
from datetime import datetime
from emailer.src.utils import get_areas_from_county

users = {
    "Items": [
        {
            'uuid': 'uuid1',
            'freq': 'hourly',
            'email': 'email1@email',
            'locations': ['All']
        },
        {
            'uuid': 'uuid2',
            'freq': 'hourly',
            'email': 'email2@email',
            'locations': ['Tyne & Wear', 'Cambridgeshire']
        },
        {
            'uuid': 'uuid3',
            'freq': 'daily',
            'email': 'email3@email',
            'locations': ['Tyne & Wear', 'Cambridgeshire', 'Greater Manchester']
        },
        {
            'uuid': 'uuid4',
            'freq': 'weekly',
            'email': 'email4@email',
            'locations': ['All']
        }
    ]
}


location_df = pd.read_csv('event-location-getter/locations.csv')


def test_user_html_hourly():
    events_df = pd.read_json('event_finder/tests/resources/test_df_reformatted.json', orient='records')
    user_df = pd.DataFrame(users['Items'])
    location_df = pd.read_csv('event-location-getter/locations.csv')





