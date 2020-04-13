import json


def test_calculate_risk_profile_should_fail_missing_content_type(tst):
    payload = {
        "age": -1,
        "dependents": 2,
        "house": {"ownership_status": "owned"},
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload))
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': 'Content-Type must be "application/json"'}


def test_calculate_risk_profile_should_fail_invalid_age(tst):
    payload = {
        "age": -1,
        "dependents": 2,
        "house": {"ownership_status": "owned"},
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'age': ['Age must be greater than 0']}}


def test_calculate_risk_profile_should_fail_invalid_dependents(tst):
    payload = {
        "age": 35,
        "dependents": -1,
        "house": {"ownership_status": "owned"},
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'dependents': ['Dependents must be greater than 0']}}


def test_calculate_risk_profile_should_fail_invalid_income(tst):
    payload = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "owned"},
        "income": -1,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'income': ['Income must be greater than 0']}}


def test_calculate_risk_profile_should_fail_invalid_marital_status(tst):
    payload = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "owned"},
        "income": 1500,
        "marital_status": "wrong",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'marital_status': ['Must be one of: single, married.']}}


def test_calculate_risk_profile_should_fail_invalid_ownership_status(tst):
    payload = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "wrong"},
        "income": 1500,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'house': {'ownership_status': ['Must be one of: owned, mortgaged.']}}}


def test_calculate_risk_profile_should_fail_invalid_risk_questions_size(tst):
    payload = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "owned"},
        "income": 1500,
        "marital_status": "married",
        "risk_questions": [0, 1],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'risk_questions': ['Shorter than minimum length 3.']}}


def test_calculate_risk_profile_should_fail_missing_mandatory_fields(tst):
    payload = {}
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 400, r_json
    assert r_json == {'message': {'age': ['Missing data for required field.'],
                                  'dependents': ['Missing data for required field.'],
                                  'income': ['Missing data for required field.'],
                                  'marital_status': ['Missing data for required field.'],
                                  'risk_questions': ['Missing data for required field.']}}


def test_calculate_risk_profile_should_work(tst):
    payload = {
        "age": 35,
        "dependents": 2,
        "house": {"ownership_status": "owned"},
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
    response = tst.client.post("/risk_profile/", data=json.dumps(payload),
                               headers={"Content-Type": "application/json"})
    r_json = response.json
    assert response.status_code == 200, r_json
    assert r_json == {
        "auto": "economic",
        "disability": "ineligible",
        "home": "economic",
        "life": "regular"
    }
