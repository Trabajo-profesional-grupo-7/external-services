from unittest.mock import patch

import pytest

from app.schemas.cities import Cities, City
from app.services.cities import parse_cities


@pytest.fixture
def mock_city_data():
    return [
        {
            "name": "Buenos Aires",
            "address": {"countryCode": "AR", "stateCode": "AR-B"},
            "geoCode": {"latitude": -34.61315, "longitude": -58.37723},
        },
        {
            "name": "Buenos Aires",
            "address": {"countryCode": "CR", "stateCode": "CR-ZZZ"},
            "geoCode": {"latitude": 9.17189, "longitude": -83.33417},
        },
        {
            "name": "Buenaventura",
            "address": {"countryCode": "CO", "stateCode": "CO-ZZZ"},
            "geoCode": {"latitude": 3.8801, "longitude": -77.03116},
        },
        {
            "name": "Paratebueno",
            "address": {"countryCode": "CO", "stateCode": "CO-ZZZ"},
            "geoCode": {"latitude": 4.37575, "longitude": -73.21547},
        },
        {
            "name": "Kotzebue",
            "address": {"countryCode": "US", "stateCode": "US-AK"},
            "geoCode": {"latitude": 66.89846, "longitude": -162.59808},
        },
        {
            "name": "Pimenta Bueno",
            "address": {"countryCode": "BR", "stateCode": "BR-RO"},
            "geoCode": {"latitude": -11.6725, "longitude": -61.19361},
        },
        {
            "name": "Kitzbuehel",
            "address": {"countryCode": "AT", "stateCode": "AT-ZZZ"},
            "geoCode": {},
        },
        {"name": "Wolfenbuettel", "address": {"countryCode": "DE"}, "geoCode": {}},
        {
            "name": "Yerba Buena",
            "address": {"countryCode": "AR", "stateCode": "AR-T"},
            "geoCode": {"latitude": -26.81667, "longitude": -65.31667},
        },
        {
            "name": "Monte Buey",
            "address": {"countryCode": "AR", "stateCode": "AR-X"},
            "geoCode": {"latitude": -32.91642, "longitude": -62.45669},
        },
    ]


def test_parse_cities(mock_city_data):
    mock_cities = mock_city_data

    with patch.object(City, "model_construct") as mock_city_construct, patch.object(
        Cities, "model_construct"
    ) as mock_cities_response:

        mock_city_instances = [
            City(
                name=city["name"],
                country=city["address"]["countryCode"],
                state_code=city["address"].get("stateCode"),
                latitude=city["geoCode"].get("latitude"),
                longitude=city["geoCode"].get("longitude"),
            )
            for city in mock_cities
            if city.get("geoCode")
        ]
        mock_city_construct.side_effect = mock_city_instances
        mock_cities_response.return_value = Cities(cities=mock_city_instances)

        result = parse_cities(mock_cities)

        assert mock_city_construct.call_count == 8
        assert mock_cities_response.call_count == 1
        assert len(result.cities) == 8
