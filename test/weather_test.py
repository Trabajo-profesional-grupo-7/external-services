from datetime import date
from unittest.mock import patch

import pytest

from app.schemas.weather import DayWeather, FiveDayWeather, Weather
from app.services.weather_services import get_location, parse_five_day_weather_info


@pytest.fixture
def mock_weather_response():
    return {
        "timelines": {
            "daily": [
                {
                    "time": "2024-06-25T09:00:00Z",
                    "values": {
                        "humidityAvg": 83.57,
                        "cloudCoverAvg": 79.48,
                        "precipitationProbabilityAvg": 4.1,
                        "temperatureAvg": 7.83,
                        "uvIndexAvg": 0,
                        "visibilityAvg": 10.33,
                    },
                },
                {
                    "time": "2024-06-26T09:00:00Z",
                    "values": {
                        "humidityAvg": 81.61,
                        "cloudCoverAvg": 16.13,
                        "precipitationProbabilityAvg": 0,
                        "temperatureAvg": 7.82,
                        "uvIndexAvg": 0,
                        "visibilityAvg": 11.25,
                    },
                },
                {
                    "time": "2024-06-27T09:00:00Z",
                    "values": {
                        "humidityAvg": 69.31,
                        "cloudCoverAvg": 44.04,
                        "precipitationProbabilityAvg": 0,
                        "temperatureAvg": 11.63,
                        "uvIndexAvg": 0,
                        "visibilityAvg": 15.66,
                    },
                },
                {
                    "time": "2024-06-28T09:00:00Z",
                    "values": {
                        "humidityAvg": 62.82,
                        "cloudCoverAvg": 15.76,
                        "precipitationProbabilityAvg": 0,
                        "temperatureAvg": 7.83,
                        "uvIndexAvg": 0,
                        "visibilityAvg": 18.65,
                    },
                },
                {
                    "time": "2024-06-29T09:00:00Z",
                    "values": {
                        "humidityAvg": 56.88,
                        "cloudCoverAvg": 2.25,
                        "precipitationProbabilityAvg": 0,
                        "temperatureAvg": 7.07,
                        "uvIndexAvg": 0,
                        "visibilityAvg": 18.65,
                    },
                },
            ]
        }
    }


def test_parse_five_day_weather_info(mock_weather_response):
    location = "SampleLocation"

    with patch.object(
        Weather, "model_construct"
    ) as mock_weather_construct, patch.object(
        DayWeather, "model_construct"
    ) as mock_day_weather_construct, patch.object(
        FiveDayWeather, "model_construct"
    ) as mock_five_day_weather_response:

        mock_weather_instances = [
            Weather(
                humidity=int(data["values"]["humidityAvg"]),
                cloudCover=int(data["values"]["cloudCoverAvg"]),
                precipitation_probability=int(
                    data["values"]["precipitationProbabilityAvg"]
                ),
                temperature=data["values"]["temperatureAvg"],
                uv_index=int(data["values"]["uvIndexAvg"]),
                visibility=data["values"]["visibilityAvg"],
            )
            for data in mock_weather_response["timelines"]["daily"]
        ]

        mock_day_weather_instances = [
            DayWeather(
                date=date.fromisoformat(data["time"][:10]),
                weather=mock_weather_instances[idx],
            )
            for idx, data in enumerate(mock_weather_response["timelines"]["daily"])
        ]

        mock_weather_construct.side_effect = mock_weather_instances
        mock_day_weather_construct.side_effect = mock_day_weather_instances
        mock_five_day_weather_response.return_value = FiveDayWeather(
            location=location, five_day_weather=mock_day_weather_instances
        )

        result = parse_five_day_weather_info(mock_weather_response, location)

        assert len(result.five_day_weather) == 5
        for i, day_weather in enumerate(result.five_day_weather):
            assert day_weather.date == date.fromisoformat(
                mock_weather_response["timelines"]["daily"][i]["time"][:10]
            )
            assert day_weather.weather.humidity == int(
                mock_weather_response["timelines"]["daily"][i]["values"]["humidityAvg"]
            )
            assert day_weather.weather.cloudCover == int(
                mock_weather_response["timelines"]["daily"][i]["values"][
                    "cloudCoverAvg"
                ]
            )
            assert day_weather.weather.precipitation_probability == int(
                mock_weather_response["timelines"]["daily"][i]["values"][
                    "precipitationProbabilityAvg"
                ]
            )
            assert (
                day_weather.weather.temperature
                == mock_weather_response["timelines"]["daily"][i]["values"][
                    "temperatureAvg"
                ]
            )
            assert day_weather.weather.uv_index == int(
                mock_weather_response["timelines"]["daily"][i]["values"]["uvIndexAvg"]
            )
            assert (
                day_weather.weather.visibility
                == mock_weather_response["timelines"]["daily"][i]["values"][
                    "visibilityAvg"
                ]
            )


def test_complete_location():
    assert (
        get_location("Cap Sarmiento", "Buenos Aires", "Argentina")
        == "Cap Sarmiento Buenos Aires Argentina"
    )


def test_missing_province():
    assert get_location("Cap Sarmiento", "", "Argentina") == "Cap Sarmiento Argentina"


def test_missing_country():
    assert get_location("Cap Sarmiento", "Argentina", "") == "Cap Sarmiento Argentina"


def test_only_city():
    assert get_location("Cap Sarmiento", "", "") == "Cap Sarmiento"


def test_only_province():
    assert get_location("", "Buenos Aires", "") == "Buenos Aires"


def test_only_country():
    assert get_location("", "", "Argentina") == "Argentina"
