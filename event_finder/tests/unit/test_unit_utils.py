import pytest
import pandas as pd
from src.utils import add_end_date_to_df

def test_add_end_date_to_df():
    # Setup
    dates = {
        "date": [
            "September 9 - September 15",
            "June 9 2024 - June 12 2024",
            "12/12/2024",
            "1/12/2024 - 10/12/2024",
            "10 October - 12 October",
            "10 October 2024 - 12 October 2024",
            "1/1 - 10/1",
            "02/05/2025",
            "06/06",
            "12 May"
    ]}

    date_df = pd.DataFrame(dates)

    # Act
    results = add_end_date_to_df(date_df)
    print(results.sort_index())

    assert str(results.loc[9, "date_end"]) == "2025-05-12 00:00:00"
    assert str(results.loc[7, "date_end"]) == "2025-05-02 00:00:00"
    assert str(results.loc[3, "date_end"]) == "2024-12-10 00:00:00"


