import unittest
from app import create_app
import json


class TestAPIProductionPlan(unittest.TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    
    def test_production_plan(self):
        """
        Test a POST request
        """
        payload = {
            "load": 910,
            "fuels":{
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [
                {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
                },
                {
                "name": "gasfiredbig2",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
                },
                {
                "name": "gasfiredsomewhatsmaller",
                "type": "gasfired",
                "efficiency": 0.37,
                "pmin": 40,
                "pmax": 210
                },
                {
                "name": "tj1",
                "type": "turbojet",
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 16
                },
                {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150
                },
                {
                "name": "windpark2",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 36
                }
            ]
        }
        
        response = self.client.post('/productionplan', data=json.dumps(payload),content_type='application/json')        
        self.assertEqual(response.status_code, 200)
        expected_result = [
            {
                "name": "windpark1",
                "p": 90.0
            },
            {
                "name": "windpark2",
                "p": 21.6
            },
            {
                "name": "gasfiredbig1",
                "p": 460.0
            },
            {
                "name": "gasfiredbig2",
                "p": 338.4
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "p": 0.0
            },
            {
                "name": "tj1",
                "p": 0.0
            }
        ]

        response_data = json.loads(response.data)
        self.assertEqual(response_data, expected_result)

    def test_missing_load_production_plan(self):
        """
        Test case when load data is missing
        Return an error
        """
        payload = {
            "fuels":{
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [
                {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
                }
            ]
        }

        response = self.client.post("/productionplan", json=payload)
        self.assertEqual(response.status_code, 400)

    
    def test_missing_fuels_production_plan(self):
        """
        Test case when fuels data are missing
        Return an error
        """
        payload = {
            "load": 480,
            "powerplants": [
                {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
                }
            ]
        }

        response = self.client.post("/productionplan", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_missing_powerplants_production_plan(self):
        """
        Test case when powerplants data are missing
        Return an error
        """
        payload = {
            "loads": 480,
            "fuels":{
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
        }

        response = self.client.post("/productionplan", json=payload)
        self.assertEqual(response.status_code, 400)

    