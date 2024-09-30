import pytest
import pandas as pd
from src.utils import get_areas_from_county

users = {
    'user1': {
        'uuid': 'uuid1',
        'frequency': 'hourly',
        'email': 'email1@email',
        'locations': ['All']
    },
    'user2': {
        'uuid': 'uuid2',
        'frequency': 'hourly',
        'email': 'email2@email',
        'locations': ['Tyne & Wear', 'Cambridgeshire']
    },
    'user3': {
        'uuid': 'uuid3',
        'frequency': 'daily',
        'email': 'email3@email',
        'locations': ['Tyne & Wear', 'Cambridgeshire', 'Greater Manchester']
    },
    'user4': {
        'uuid': 'uuid4',
        'frequency': 'weekly',
        'email': 'email4@email',
        'locations': ['All']
    }
}



events_df = pd.read_json('event_finder/tests/resources/test_df_reformatted.json', orient='records')
user_df = pd.DataFrame(users)
location_df = pd.read_csv('event-location-getter/locations.csv', index_col=0)
for user in user_df.iterrows():
    print(get_areas_from_county(user, location_df))
