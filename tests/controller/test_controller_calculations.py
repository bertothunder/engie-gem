import os
import json
from api.services.production_plan.controller import process


dataset_path = os.path.dirname(os.path.abspath(__file__))


# NOTE: None of the tests above will check for input format, since this is performed at the API level.
# Only for the functional part of it.

def test_standard_powerset_calculations():
    """
    Tests the calculations wfo an standard power load case
    """
    json_file = os.path.join(dataset_path, '../datasets', 'power_normal_load.json')
    with open(json_file, 'r') as f:
        data = json.load(f)

    result = process(data)

    expected_data = [
        {
            'name': 'windpark1',
            'p': 90,
        },
        {
            'name': 'windpark2',
            'p': 22,
        },
        {
            'name': 'gasfiredbig1',
            'p': 244,
        },
        {
            'name': 'gasfiredbig2',
            'p': 125,
        },
        {
            'name': 'gasfiredsomewhatsmaller',
            'p': 0,
        },
        {
            'name': 'tj1',
            'p': 0,
        }
    ]

    assert result == expected_data


def test_little_load_powerset_calculations():
    """
    Tests the calculations when little load is required from the system.
    In this case, wind plants will cover the required load.
    """
    json_file = os.path.join(dataset_path, '../datasets', 'power_little_load.json')
    with open(json_file, 'r') as f:
        data = json.load(f)

    result = process(data)

    expected_data = [
        {
            'name': 'windpark1',
            'p': 40,
        },
        {
            'name': 'windpark2',
            'p': 0,
        },
        {
            'name': 'gasfiredbig1',
            'p': 0,
        },
        {
            'name': 'gasfiredbig2',
            'p': 0,
        },
        {
            'name': 'gasfiredsomewhatsmaller',
            'p': 0,
        },
        {
            'name': 'tj1',
            'p': 0,
        }
    ]

    assert result == expected_data


def test_little_load_powerset_no_wind_efficiency():
    """
    Tests the calculations when no wind efficiency is given, which will actually put the next plants into the grid.
    """
    json_file = os.path.join(dataset_path, '../datasets', 'power_no_wind_efficiency.json')
    with open(json_file, 'r') as f:
        data = json.load(f)

    result = process(data)

    expected_data = [
        {
            'name': 'gasfiredbig1',
            'p': 100,
        },
        {
            'name': 'windpark1',
            'p': 0,
        },
        {
            'name': 'windpark2',
            'p': 0,
        },
        {
            'name': 'gasfiredbig2',
            'p': 0,
        },
        {
            'name': 'gasfiredsomewhatsmaller',
            'p': 0,
        },
        {
            'name': 'tj1',
            'p': 0,
        }
    ]

    assert result == expected_data


def test_no_load_powerset_calculations():
    # This is an easy case: no load, no power in the grid from any plant
    json_file = os.path.join(dataset_path, '../datasets', 'power_no_load.json')
    with open(json_file, 'r') as f:
        data = json.load(f)

    result = process(data)

    expected_data = [
        {
            'name': 'windpark1',
            'p': 0,
        },
        {
            'name': 'windpark2',
            'p': 0,
        },
        {
            'name': 'gasfiredbig1',
            'p': 0,
        },
        {
            'name': 'gasfiredbig2',
            'p': 0,
        },
        {
            'name': 'gasfiredsomewhatsmaller',
            'p': 0,
        },
        {
            'name': 'tj1',
            'p': 0,
        }
    ]

    assert result == expected_data


def test_huge_load_powerset_calculations():
    """
    Tests the case when a huge amount is required, which will not be covered by all the stations (given the
    efficiency and conversion factors. All plants will come into the grid, but the total load won't be covered
    """
    json_file = os.path.join(dataset_path, '../datasets', 'power_huge_load.json')
    with open(json_file, 'r') as f:
        data = json.load(f)

    result = process(data)

    expected_data = [
        {
            'name': 'windpark1',
            'p': 90,
        },
        {
            'name': 'windpark2',
            'p': 22,
        },
        {
            'name': 'gasfiredbig1',
            'p': 244,
        },
        {
            'name': 'gasfiredbig2',
            'p': 244,
        },
        {
            'name': 'gasfiredsomewhatsmaller',
            'p': 78,
        },
        {
            'name': 'tj1',
            'p': 5,
        }
    ]

    assert result == expected_data
    assert sum([item['p'] for item in result]) <= data['load']
