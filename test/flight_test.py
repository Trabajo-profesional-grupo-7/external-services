from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.ext.amadeus import get_flight_info
from app.main import app
from app.utils.api_exception import APIException
from app.utils.constants import *

client = TestClient(app)


def test_flight_information():

    test_carrier_code = "AA"
    test_flight_number = "900"
    test_departure_date = "2024-02-18"

    with patch("app.ext.amadeus.get_flight_info") as mock_get:
        mock_get.return_value = "[{'type': 'DatedFlight', 'scheduledDepartureDate': '2024-02-07', 'flightDesignator': {'carrierCode': 'AA', 'flightNumber': 900}, 'flightPoints': [{'iataCode': 'EZE', 'departure': {'timings': [{'qualifier': 'STD', 'value': '2024-02-07T21:35-03:00'}]}}, {'iataCode': 'MIA', 'arrival': {'timings': [{'qualifier': 'STA', 'value': '2024-02-08T05:00-05:00'}]}}], 'segments': [{'boardPointIataCode': 'EZE', 'offPointIataCode': 'MIA', 'scheduledSegmentDuration': 'PT9H25M'}], 'legs': [{'boardPointIataCode': 'EZE', 'offPointIataCode': 'MIA', 'aircraftEquipment': {'aircraftType': '77W'}, 'scheduledLegDuration': 'PT9H25M'}]}]"

    response = client.get(
        f"/flights/status?carrier_code={test_carrier_code}&flight_number={test_flight_number}&departure_date={test_departure_date}"
    )

    assert response.status_code == 200

    assert "flight_departure_date" in response.json()
    assert "flight_departure_time" in response.json()
    assert "flight_arrival_date" in response.json()
    assert "flight_arrival_time" in response.json()
    assert "departure_airport" in response.json()
    assert "arrival_airport" in response.json()


def test_flight_information_api_exception():
    test_carrier_code = "AA"
    test_flight_number = "700"
    test_departure_date = "2024-01-30"

    with patch("app.ext.amadeus.get_flight_info") as mock_get:
        mock_get.side_effect = APIException(
            code=FLIGTH_INFO_NOT_FOUND_ERROR, msg="FLIGHT INFORMATION NOT FOUND"
        )
    response = client.get(
        f"/flights/status?carrier_code={test_carrier_code}&flight_number={test_flight_number}&departure_date={test_departure_date}"
    )

    assert response.status_code == 404
