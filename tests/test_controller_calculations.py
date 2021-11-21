import os
import json
from api.services.production_plan.controller import process


dataset_path = os.path.dirname(os.path.abspath(__file__))


# NOTE: None of the tests above will check for input format, since this is performed at the API level.
# Only for the functional part of it.

def test_powerset_1_calculations():
    power_1_json = os.path.join(dataset_path, 'dataset', 'power1.json')
    with open(power_1_json, 'r') as f:
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


def test_powerset_2_calculations_little_load():
    # Since merit-order algorithm gives more weight on efficiency than cost, when the required load is low enough,
    # most-efficient plans are given priority in the production, even when cost is higher.
    power_1_json = os.path.join(dataset_path, 'dataset', 'power2.json')
    with open(power_1_json, 'r') as f:
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
            'p': 40,
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


def test_powerset_3_calculations_on_no_load():
    # This is an easy case: no load, no power in the grid from any plant
    power_1_json = os.path.join(dataset_path, 'dataset', 'power3.json')
    with open(power_1_json, 'r') as f:
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

