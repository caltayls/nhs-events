import pytest
from datetime import datetime
import pandas as pd
from src.utils import add_end_date_to_df

def test_add_end_date_to_df(mocker):
    # Setup
    mock_datetime = mocker.Mock()
    mock_datetime.datetime.now.return_value = datetime(2024, 9, 1)
    mocker.patch("src.utils.datetime", mock_datetime)
    dates = {
        "date": [
            "June 9 2024 - June 12 2024",
            "12/12/2024",
            "1/12/2024 - 10/12/2024",
            "10 October - 15 October",
            "10 October 2024 - 12 October 2024",
            "1/1 - 10/1",
            "02/05/2025",
            "06/06",
            "12 May",
            "September 7, 2024",
    ]}

    date_df = pd.DataFrame(dates)

    # Act
    results = add_end_date_to_df(date_df)

    # Assert
    assert str(results.loc[8, "date_end"]) == "2025-05-12 00:00:00"
    assert str(results.loc[6, "date_end"]) == "2025-05-02 00:00:00"
    assert str(results.loc[3, "date_end"]) == "2024-10-15 00:00:00"
    assert str(results.loc[9, "date_end"]) == "2024-09-07 00:00:00"


