from agents import function_tool


@function_tool
def  get_weather(city:str , temperature:int)->int:
    return f" the temperature of {city} is {temperature}"