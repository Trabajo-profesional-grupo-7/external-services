from datetime import datetime
from unittest.mock import patch

import pytest

from app.services.flight_services import *
from app.utils.api_exception import APIException
from app.utils.constants import *

mock_response = {
    "type": "DatedFlight",
    "scheduledDepartureDate": "2024-06-25",
    "flightDesignator": {"carrierCode": "AA", "flightNumber": 900},
    "flightPoints": [
        {
            "iataCode": "EZE",
            "departure": {
                "timings": [{"qualifier": "STD", "value": "2024-06-25T20:55-03:00"}]
            },
        },
        {
            "iataCode": "MIA",
            "arrival": {
                "timings": [{"qualifier": "STA", "value": "2024-06-26T05:05-04:00"}]
            },
        },
    ],
    "segments": [
        {
            "boardPointIataCode": "EZE",
            "offPointIataCode": "MIA",
            "scheduledSegmentDuration": "PT9H10M",
        }
    ],
    "legs": [
        {
            "boardPointIataCode": "EZE",
            "offPointIataCode": "MIA",
            "aircraftEquipment": {"aircraftType": "772"},
            "scheduledLegDuration": "PT9H10M",
        }
    ],
}


def test_parse_flight_info():
    expected_departure_date = datetime.strptime("2024-06-25", "%Y-%m-%d").date()
    expected_departure_time = datetime.strptime(
        "2024-06-25T20:55-03:00", "%Y-%m-%dT%H:%M%z"
    ).time()
    expected_arrival_date = datetime.strptime("2024-06-26", "%Y-%m-%d").date()
    expected_arrival_time = datetime.strptime(
        "2024-06-26T05:05-04:00", "%Y-%m-%dT%H:%M%z"
    ).time()
    expected_departure_airport = "EZE"
    expected_arrival_airport = "MIA"

    with patch(
        "app.services.flight_services.parse_flight_info"
    ) as mock_parse_flight_info:
        mock_parse_flight_info.return_value = {
            "flight_departure_date": expected_departure_date,
            "flight_departure_time": expected_departure_time,
            "flight_arrival_date": expected_arrival_date,
            "flight_arrival_time": expected_arrival_time,
            "departure_airport": expected_departure_airport,
            "arrival_airport": expected_arrival_airport,
        }

        result = parse_flight_info(mock_response)

    assert result.flight_departure_date == expected_departure_date
    assert result.flight_departure_time == expected_departure_time
    assert result.flight_arrival_date == expected_arrival_date
    assert result.flight_arrival_time == expected_arrival_time
    assert result.departure_airport == expected_departure_airport
    assert result.arrival_airport == expected_arrival_airport
