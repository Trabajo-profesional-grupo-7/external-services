def get_user_city(data: dict):
    address = data.get("address", {})
    suburb = address.get("suburb", None)
    city = address.get("city", None)
    town = address.get("town", None)
    state = address.get("state", None)
    country = address.get("country", None)

    address_components = [suburb, city, town, state, country]

    city = ", ".join(filter(None, address_components))

    if city:
        return city
    else:
        return None
