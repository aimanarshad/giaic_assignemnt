from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, input_guardrail


@input_guardrail
def reject_Indian_cites(input_user:str):
    indian_cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Pune", "Ahmedabad"]
    for city in indian_cities:
        if city.lower in input_user.lower:
            raise InputGuardrailTripwireTriggered(
                "Agent must reject queries about Indian Cities"
             )
    return input_user



