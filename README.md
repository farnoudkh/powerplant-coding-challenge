# Setting Up the powerplant API for the coding challenge

This document will guide you through the steps to set up and launch the application.


### Prerequisites 
Install on your computer:
- Python 3.8 or higher
- pip (Python's package installer)

### Setting Up
After cloning the project, navigate to the project directory (powerplant-coding-challenge)

```
cd powerplant-coding-challenge
```

Create a virtual environment

- If you are using Windows: 

    ```
    python3 -m venv venv
    ```

    Activate the virtual environment:

    ```
    .\venv\Scripts\activate
    ```

- If you are using Linux or MacOS:
    
    ```
    python3 -m venv venv
    ```
    ```
    source venv/bin/activate
    ```

Install the required dependencies:

```
pip install -r requirements.txt
```

### Launch the application
To start the application, use the command : 

```
python run.py
```

The terminal will display: Running on http://127.0.0.1:8888

### Use curl to send request

Open another terminal at the same place and paste the following request (This is from example_payloads/payload3.json)

```
curl -i -X POST http://127.0.0.1:8888/productionplan \
    -H "Content-Type: application/json" \
    -d '{
  "load": 910,
  "fuels":
  {
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
}'
```

### Run unit and functional tests

The folder *tests* contains the unit and functional tests.
You can test the application by running these tests :

```
python -m unittest discover tests/
```