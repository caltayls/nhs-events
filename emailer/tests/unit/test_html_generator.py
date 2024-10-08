import pytest
import pandas as pd

from emailer.src.html_generator import render_html

def test_render_html():
    # Setup
    events = [
        {
            "event_name": "Old Time Sailors",
            "location": "Trentham Gardens Amphitheatre",
            "date": "September 1, 2024",
            "url": "https://www.concertsforcarers.org.uk/events/old-time-sailors-4704-trentham-gardens-amphitheatre-sep-1-2024",
            "website_name": "concertsforcarers",

        },
        {
            "event_name": "Hot Wheels\u00e2\u0084\u00a2 City Experience (Add a total of 8 Tickets to the ballot!) - Hot Wheels\u00e2\u0084\u00a2 City Experience",
            "location": "B.E.C Arena, Manchester",
            "date": "September 2, 2024",
            "url": "https://www.concertsforcarers.org.uk/events/hot-wheels-city-experience-add-a-total-of-8-tickets-to-the-ballot-4685-bec-arena-manchester-sep-2-2024",
            "website_name": "concertsforcarers",
        },
        {
            "event_name": "Hot Wheels\u00e2\u0084\u00a2 City Experience (Add a total of 8 Tickets to the ballot!) - Hot Wheels\u00e2\u0084\u00a2 City Experience",
            "location": "B.E.C Arena, Manchester",
            "date": "September 3, 2024",
            "url": "https://www.concertsforcarers.org.uk/events/hot-wheels-city-experience-add-a-total-of-8-tickets-to-the-ballot-4686-bec-arena-manchester-sep-3-2024",
            "website_name": "concertsforcarers",
        }
    ]
    df = pd.DataFrame(events)

    # Act
    actual = str(render_html(df).encode('utf-8'))


    expected_section1 = "<td><a href=https://www.concertsforcarers.org.uk/events/old-time-sailors-4704-trentham-gardens-amphitheatre-sep-1-2024>Old Time Sailors</a></td>"
    expected_section2 = "<td>Trentham Gardens Amphitheatre</td>"
    expected_section3 = "<td>September 1, 2024</td>"
    expected_section4 = "<td>concertsforcarers</td>"

    assert expected_section1 in actual
    assert expected_section2 in actual
    assert expected_section3 in actual
    assert expected_section4 in actual

    



