from app.schemas.cities import *


def parse_cities(cities):
    all_cities = []

    for city in cities:
        if city["geoCode"]:
            all_cities.append(
                City.model_construct(
                    name=city["name"],
                    country=city["address"]["countryCode"],
                    state_code=city["address"]["stateCode"],
                    latitude=city["geoCode"]["latitude"],
                    longitude=city["geoCode"]["longitude"],
                )
            )

    return Cities.model_construct(cities=all_cities)
