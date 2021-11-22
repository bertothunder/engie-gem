import json


def test_api_prod_plan_no_post_methods_request_returns_405(client):
    """
    Asserts any request to the api other than POST will return 405
    :param client:
    :return:
    """
    path = "/productionplan"
    response = client.get(path)
    assert response.status_code == 405
    response = client.delete(path)
    assert response.status_code == 405
    response = client.head(path)
    assert response.status_code == 405
    response = client.put(path)
    assert response.status_code == 405


def test_api_prod_plan_missing_fields_will_return_422(client, missing_load_dataset):
    response = client.post("/productionplan", data=missing_load_dataset)
    assert response.status_code == 422
    # The value below will work for any of the other fields, showing it in 'loc' field.
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "load"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_api_prod_plan_invalid_int_field_vaue_will_return_422(client, invalid_int_value_dataset):
    response = client.post("/productionplan", data=invalid_int_value_dataset)
    assert response.status_code == 422
    # The value below will work for any of the other fields, showing it in 'ctx' field.
    assert response.json() == {
        "detail": [
            {
                "ctx": {
                    "colno": 13,
                    "doc": "\n"
                    "        {\n"
                    '            "load": 400,\n'
                    '            "fuels":\n'
                    "                {\n"
                    '                    "gas(euro/MWh)": 13.4,\n'
                    '                    "kerosine(euro/MWh)": 50.8,\n'
                    '                    "co2(euro/ton)": 20,\n'
                    '                    "wind(%)": 60\n'
                    "                },\n"
                    '            "powerplants": [\n'
                    "                {\n"
                    '                    "name": "gasfiredbig1",\n'
                    '                    "type": "gasfired",\n'
                    '                    "efficiency": 0.53,\n'
                    '                    "pmin": "100",\n'
                    '                    "pmax": 460\n'
                    "                },\n"
                    "            ]\n"
                    "        }\n"
                    "    ",
                    "lineno": 19,
                    "msg": "Expecting value",
                    "pos": 529,
                },
                "loc": ["body", 529],
                "msg": "Expecting value: line 19 column 13 (char 529)",
                "type": "value_error.jsondecode",
            }
        ]
    }


def test_api_prod_plan_normal_json_data(client, normal_json_dataset):
    response = client.post("/productionplan", data=normal_json_dataset)
    assert response.status_code == 200
    assert response.json() == [
        {"name": "windpark1", "p": 90},
        {"name": "windpark2", "p": 22},
        {"name": "gasfiredbig1", "p": 244},
        {"name": "gasfiredbig2", "p": 125},
        {"name": "gasfiredsomewhatsmaller", "p": 0},
        {"name": "tj1", "p": 0},
    ]
