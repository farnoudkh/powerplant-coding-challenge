from flask import Flask, request, jsonify
from .services import calculate_cost, merit_order, production_plan

app = Flask(__name__)

@app.route('/productionplan', methods=["POST"])
def production_plan_api():
    """
    Creates a production plan on the provided datas.
    It expectes a POST request with a JSON body containing the following datas: 
        "loads" (float): The total energy
        fuels (dict): A dictionnary representing the fuel coasts
        powerplant (dict): A dictionnary representing the powerplant containing the following informations: 

    Returns: 
        Response (json): A JSON response containing the production plan.
        If successful, 200 status code is returned.
        If there is an error in the datas, 400 status code is returned.
        If there is a server error, 500 status code is returned
    """
    try:
        data = request.json
        load = data.get('load')
        fuels = data.get('fuels')
        powerplants = data.get('powerplants')
        if not load or not fuels or not powerplants:
            return jsonify({"error": "Error"}), 400
        result = production_plan(load, fuels, powerplants)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
