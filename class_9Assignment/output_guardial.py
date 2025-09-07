from agents import  OutputGuardrailTripwireTriggered

import output_guardial


@output_guardial
def reject_US_cites(output_user:str):
    us_cities = [
    "New York City",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
    "Austin"]
    for city in us_cities:
        if city.lower in output_user.lower:
            raise OutputGuardrailTripwireTriggered(
                "Agent Must not respond with any U.S. city weather."
             )
    return output_user



