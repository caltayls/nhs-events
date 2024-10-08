import json
import pytest
import pandas as pd
from boto3.dynamodb.conditions import Key
from emailer.src import utils

@pytest.fixture
def mock_datetime(mocker):
    def _mock_datetime(hour, weekday):
        mock_datetime = mocker.patch("emailer.src.utils.datetime")
        mock_dt = mocker.Mock()
        mock_dt.hour = hour
        mock_dt.weekday.return_value = weekday
        mock_datetime.today.return_value = mock_dt
    return _mock_datetime


def test_get_areas_from_county():
    # Setup
    users = [
    {'locations': ['All']},
    {'locations': ['Tyne & Wear', 'Cambridgeshire']},
    {'locations': ['Tyne & Wear', 'Cambridgeshire', 'Greater Manchester']}
]
    location_df = pd.read_csv('event-location-getter/locations.csv')
    user_df = pd.DataFrame(users)
    
    # Act 
    expected_area_counts = [458, 5, 47]
    for i, row in user_df.iterrows():
        user_areas = utils.get_areas_from_county(row, location_df)
       
        # Shoud cache this       
        print('|'.join(user_areas.values))
        actual_count = len(user_areas)
        
        # Assert
        assert actual_count == expected_area_counts[i]



def test_get_users_hourly(mocker, mock_datetime):
    # Setup
    mock_dynamo = mocker.Mock()
    mock_table = mocker.MagicMock()
    mock_table.query.return_value = {"Items": []}
    mock_dynamo.Table.return_value = mock_table
    mocker.patch("boto3.client", return_value=mock_dynamo)

    mock_datetime(hour=10, weekday=0)

    # Act
    actual = utils.get_users()

    #Assert
    calls = mock_table.query.call_args_list
    assert calls[0][1]['KeyConditionExpression']._values[1] == 'hourly'


def test_get_users_daily(mocker, mock_datetime):
    # Setup
    mock_dynamo = mocker.Mock()
    mock_table = mocker.MagicMock()
    mock_table.query.return_value = {"Items": []}
    mock_dynamo.Table.return_value = mock_table
    mocker.patch("boto3.client", return_value=mock_dynamo)

    mock_datetime(hour=17, weekday=0)

    # Act
    actual = utils.get_users()

    # Assert
    calls = mock_table.query.call_args_list
    assert calls[0][1]['KeyConditionExpression']._values[1] == 'hourly'
    assert calls[1][1]['KeyConditionExpression']._values[1] == 'daily'

def test_get_users_weekly(mocker, mock_datetime):
    # Setup
    mock_dynamo = mocker.Mock()
    mock_table = mocker.MagicMock()
    mock_table.scan.return_value = {"Items": []}
    mock_dynamo.Table.return_value = mock_table
    mocker.patch("boto3.client", return_value=mock_dynamo)

    mock_datetime(hour=17, weekday=4)

    # Act
    actual = utils.get_users()

    # Assert
    mock_table.scan.assert_called_once()

