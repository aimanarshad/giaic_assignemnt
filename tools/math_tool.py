
from agents import function_tool


@function_tool
def addition(a:int,b:int)-> str :
    "add two numbers and return value"

    print("Addition done ")
    return a+b


@function_tool
def subraction(a:int,b:int)-> str :
    "subtract two numbers and return value"

    print("Subraction done ")
    return a-b

@function_tool
def multiply(a:int,b:int)-> str :
    "multiply two numbers and return value"

    print("Multiplication done ")
    return a*b

@function_tool
def division(a:int,b:int)-> str :
    "divide two numbers and return value"

    print("Division done ")
    return a/b



