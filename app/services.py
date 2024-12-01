# Calculate cost and production plan

def calculate_cost(powerplant, fuels):
    """
    Calculates the cost of producing electricity for a given powerplant
    Parameters:
        powerplant (dict): A dictionnary representing the powerplant containing the following informations: 
            - "type" (str): The type of the powerplant (example : gasfired, turbojet, windturbine)
            - "efficiency" (float): The efficiency of the powerplant
            - "pmin" (float): The minimum of power of the powerplant
            - "pmax" (float): The maximum of power of the powerplant
        fuels (dict): A dictionnary representing the fuel coasts
            - "gas(euro/MWh)" (float): The cost of gas per MWh
            - "kerosine(euro/MWh)" (float): The cost of kerosene per MWh
            - "co2(euro/ton)" (float): The cost of CO2 emissions per ton
            - "wind(%)" (float): The percentage of wind energy available
    Returns:
        float : Cost of producing electricity
    """

    if powerplant["type"] == "gasfired":
        return fuels["gas(euro/MWh)"] / powerplant["efficiency"]
    elif powerplant["type"] == "turbojet":
        return fuels["kerosine(euro/MWh)"] / powerplant["efficiency"]
    elif powerplant["type"] == "windturbine":
        return 0
    return None

def get_powerplant_cost(powerplant, fuels):
    """
    Get the cost of a powerplant.
    Parameters:
        powerplant (dict): A dictionnary representing the powerplant
        fuels (dict): A dictionnary representing the fuel coasts
    Returns:
        float: The cost of the powerplant as calculated by the 'calculate_cost()' function.
    """
    return calculate_cost(powerplant, fuels)

def merit_order(powerplants, fuels):
    """
    Sort the powerplants by their costs
    Parameters:
        powerplant (dict): A dictionnary representing the powerplant
        fuels (dict): A dictionnary representing the fuel coasts
    Returns:
        list: The list of powerplants sorted by costs
    """
    sorted_powerplants = sorted(powerplants, key=lambda p: get_powerplant_cost(p, fuels))
    return sorted_powerplants

def production_plan(load, fuels, powerplants):
    """
    Calculates a production plan and selecting powerplant based on their cost and availability
    Parameters:
        load (float): The total energy
        fuels (dict): A dictionnary representing the fuel coasts
            - "gas(euro/MWh)" (float): The cost of gas per MWh
            - "kerosine(euro/MWh)" (float): The cost of kerosene per MWh
            - "co2(euro/ton)" (float): The cost of CO2 emissions per ton
            - "wind(%)" (float): The percentage of wind energy available
        powerplant (dict): A dictionnary representing the powerplan containing the following informations: 
            - "type" (str): The type of the powerplant (example : gasfired, turbojet, windturbine)
            - "efficiency" (float): The efficiency of the powerplant
            - "pmin" (float): The minimum of power of the powerplant
            - "pmax" (float): The maximum of power of the powerplant
    Returns:
        list : List of dictionnary having as key, the name of the powerplant and as value, the generated power.
    """
    # Sort the powerplants by production cost
    try:
        sorted_powerplants = merit_order(powerplants, fuels)
        result = []
        remaining_load = load
        for powerplant in sorted_powerplants:
            if powerplant["type"] == "windturbine":
                # Calcul the generated power for a windturbine 
                generated_power = min(remaining_load, powerplant["pmax"] * (fuels["wind(%)"] / 100))
                print(generated_power)
            else:
                # Calcul the generated power for a gasfired or turbinejet 
                generated_power = min(remaining_load, powerplant["pmax"])
            
            result.append({"name": powerplant["name"], "p": round(generated_power, 1)})
            remaining_load -= generated_power
    except Exception as e:
        print(f'Error in production plan: {e}')
    return result