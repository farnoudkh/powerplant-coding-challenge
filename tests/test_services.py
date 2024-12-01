import unittest
from app import create_app
from app.services import calculate_cost, merit_order, production_plan


class TestUnitProductionPlan(unittest.TestCase):

    def setUp(self):
        """
        Set up the variables for all test cases
        """

        self.client = create_app().test_client()
        self.fuels =   {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        }


    def test_cost_calculation_gas_fired(self):
        """
        Calcul the cost for a gasfired powerplant
        """
        powerplant = {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        }
        calculated_cost = calculate_cost(powerplant, self.fuels)
        expected_cost = self.fuels["gas(euro/MWh)"] / powerplant["efficiency"]
        self.assertEqual(calculated_cost, expected_cost)

    def test_cost_calculation_turbojet(self):
        """
        Calcul the cost for a turbojet powerplant
        """
        powerplant = {
            "name": "tj1",
            "type": "turbojet",
            "efficiency": 0.3,
            "pmin": 0,
            "pmax": 16
        }
        calculated_cost = calculate_cost(powerplant, self.fuels)
        expected_cost = self.fuels["kerosine(euro/MWh)"] / powerplant["efficiency"]
        self.assertEqual(calculated_cost, expected_cost)
    
    def test_calculate_cost_windturbine(self):
        """
        Calcul the cost for a windturbine powerplant
        """
        plant = {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
        }
        expected_cost = 0
        calculated_cost = calculate_cost(plant, self.fuels)
        self.assertEqual(calculated_cost, expected_cost)

    def test_merit_order(self):
        """
        Sort the powerplants
        """
        powerplants = [
            {
                "name": "gasfiredbig1", 
                "type": "gasfired", 
                "efficiency": 0.53, 
                "pmin": 100, 
                "pmax": 460, 
            },
            {
                "name": "tj1", 
                "type": "turbojet", 
                "efficiency": 0.3, 
                "pmin": 0, 
                "pmax": 16,
            },
            {
                "name": "windpark1", 
                "type": "windturbine", 
                "efficiency": 1, 
                "pmin": 0, 
                "pmax": 150, 
            }
        ]

        # Calculate the cost for each powerplant
        for powerplant in powerplants:
            powerplant['cost'] = calculate_cost(powerplant, self.fuels)
            print(powerplant)
        sorted_plants = merit_order(powerplants, self.fuels)
        assert sorted_plants[0]['name'] == 'windpark1'
        assert sorted_plants[1]['name'] == 'gasfiredbig1'
        assert sorted_plants[2]['name'] == 'tj1'


    def test_production_plan(self):
        """
        Calculate a production plan for powerplants and a given load
        """
        powerplants = [
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
        
        load = 910
        result = production_plan(load, self.fuels, powerplants)

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
        # Fixing issues because of decimals to compare with 1 decimal
        for i in range(len(result)):
            r = result[i]
            e = expected_result[i]

            self.assertEqual(r["name"], e["name"])
            self.assertAlmostEqual(r["p"], e["p"], places=1)

if __name__ == '__main__':
    unittest.main()