import operator
import json
import requests

class ToolBox:
    def __init__(self):
        self.tools_dict = {}
    
    def store(self, function_list):
        for function in function_list:
            self.tools_dict[function.__name__] = function.__doc__
    
    def tools(self):
        tools_str = ""
        for name, doc in self.tools_dict.items():
            tools_str += f"{name}: {doc}\n"
        return tools_str.strip()

def basic_calculator(input_str):
    """
    Perform a numeric operation on two numbers based on the input string or dictionary.

    Parameters:
    input_str (str or dict): Either a JSON string representing a dictionary with keys 'num1', 'num2', and 'operation',
                            or a dictionary directly. Example: '{"num1": 5, "num2": 3, "operation": "add"}'
                            or {"num1": 67869, "num2": 9030393, "operation": "divide"}

    Returns:
    str: The formatted result of the operation.

    Raises:
    Exception: If an error occurs during the operation (e.g., division by zero).
    ValueError: If an unsupported operation is requested or input is invalid.
    """
    try:
        # Handle both dictionary and string inputs
        if isinstance(input_str, dict):
            input_dict = input_str
        else:
            # Clean and parse the input string
            input_str_clean = input_str.replace("'", "\"")
            input_str_clean = input_str_clean.strip().strip("\"")
            input_dict = json.loads(input_str_clean)
        
        # Validate required fields
        if not all(key in input_dict for key in ['num1', 'num2', 'operation']):
            return "Error: Input must contain 'num1', 'num2', and 'operation'"

        num1 = float(input_dict['num1'])  # Convert to float to handle decimal numbers
        num2 = float(input_dict['num2'])
        operation = input_dict['operation'].lower()  # Make case-insensitive
    except (json.JSONDecodeError, KeyError) as e:
        return "Invalid input format. Please provide valid numbers and operation."
    except ValueError as e:
        return "Error: Please provide valid numerical values."

    # Define the supported operations with error handling
    operations = {
        'add': operator.add,
        'plus': operator.add,  # Alternative word for add
        'subtract': operator.sub,
        'minus': operator.sub,  # Alternative word for subtract
        'multiply': operator.mul,
        'times': operator.mul,  # Alternative word for multiply
        'divide': operator.truediv,
        'floor_divide': operator.floordiv,
        'modulus': operator.mod,
        'power': operator.pow,
        'lt': operator.lt,
        'le': operator.le,
        'eq': operator.eq,
        'ne': operator.ne,
        'ge': operator.ge,
        'gt': operator.gt
    }

    # Check if the operation is supported
    if operation not in operations:
        return f"Unsupported operation: '{operation}'. Supported operations are: {', '.join(operations.keys())}"

    try:
        # Special handling for division by zero
        if (operation in ['divide', 'floor_divide', 'modulus']) and num2 == 0:
            return "Error: Division by zero is not allowed"

        # Perform the operation
        result = operations[operation](num1, num2)
        
        # Format result based on type
        if isinstance(result, bool):
            result_str = "True" if result else "False"
        elif isinstance(result, float):
            # Handle floating point precision
            result_str = f"{result:.6f}".rstrip('0').rstrip('.')
        else:
            result_str = str(result)

        return f"The answer is: {result_str}"
    except Exception as e:
        return f"Error during calculation: {str(e)}"

def reverse_string(input_string):
    """
    Reverse the given string.

    Parameters:
    input_string (str): The string to be reversed.

    Returns:
    str: The reversed string.
    """
    # Check if input is a string
    if not isinstance(input_string, str):
        return "Error: Input must be a string"
    
    # Reverse the string using slicing
    reversed_string = input_string[::-1]
    
    # Format the output
    result = f"The reversed string is: {reversed_string}"
    
    return result

def get_bangkok_weather(input_str=""):
    """
    Get the current weather conditions in Bangkok, Thailand.

    Parameters:
    input_str (str): Optional input (not used, can be empty string or any value)

    Returns:
    str: Current weather information for Bangkok including temperature, humidity, and conditions.
    """
    try:
        # Using OpenWeatherMap free API for Bangkok
        # Using a free weather API that doesn't require API key
        api_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 13.7563,  # Bangkok latitude
            "longitude": 100.5018,  # Bangkok longitude
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "Asia/Bangkok"
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get('current', {})
        
        # Weather code mapping (simplified)
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail"
        }
        
        temperature = current.get('temperature_2m', 'N/A')
        humidity = current.get('relative_humidity_2m', 'N/A')
        wind_speed = current.get('wind_speed_10m', 'N/A')
        weather_code = current.get('weather_code', 0)
        weather_desc = weather_codes.get(weather_code, "Unknown conditions")
        
        result = f"Current weather in Bangkok, Thailand:\n"
        result += f"Temperature: {temperature}°C\n"
        result += f"Humidity: {humidity}%\n"
        result += f"Wind Speed: {wind_speed} km/h\n"
        result += f"Conditions: {weather_desc}"
        
        return result
        
    except requests.RequestException as e:
        return f"Error fetching weather data: Unable to connect to weather service. {str(e)}"
    except Exception as e:
        return f"Error processing weather data: {str(e)}"
