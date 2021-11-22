import pytest
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api import create_app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def app(event_loop) -> FastAPI:
    """
    FastAPI app for use in tests
    :return:
    """
    app = create_app(testing=True)
    yield app


@pytest.fixture(scope="function")
def client(app: FastAPI) -> TestClient:
    """
    Returns a default FastAPI test client
    :param app:
    :return:
    """
    yield TestClient(app)


@pytest.fixture(scope="function")
def missing_load_dataset():
    # No load
    return """
        {
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
                }
            ]
        }
    """


@pytest.fixture(scope="function")
def invalid_int_value_dataset():
    return """
        {
            "load": 400,
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
                    "pmin": "100",
                    "pmax": 460
                },
            ]
        }
    """


@pytest.fixture(scope="function")
def normal_json_dataset():
    return """
        {
      "load": 480,
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
    }"""
