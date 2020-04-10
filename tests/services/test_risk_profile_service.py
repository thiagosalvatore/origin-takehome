from datetime import datetime

from origin_test.services.risk_profile import RiskProfileService


def test_calculate_age_score_should_deduct_one():
    profile = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "wrong"},
        "income": 1500,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_age_score()

    assert score == {
        "auto": -1,
        "disability": -1,
        "home": -1,
        "life": -1
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_age_score_should_deduct_two():
    profile = {
        "age": 25,
        "dependents": 1,
        "house": {"ownership_status": "wrong"},
        "income": 1500,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_age_score()

    assert score == {
        "auto": -2,
        "disability": -2,
        "home": -2,
        "life": -2
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_age_score_should_be_ineligible_due_to_age():
    profile = {
        "age": 61,
        "dependents": 1,
        "house": {"ownership_status": "wrong"},
        "income": 1500,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_age_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "ineligible",
        "home": "economic",
        "life": "ineligible"
    }


def test_calculate_income_score_high_should_deduct_one_from_everything():
    profile = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "wrong"},
        "income": 201000,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_income_score()

    assert score == {
        "auto": -1,
        "disability": -1,
        "home": -1,
        "life": -1
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_income_score_low_should_do_nothing():
    profile = {
        "age": 35,
        "dependents": 1,
        "house": {"ownership_status": "wrong"},
        "income": 20,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_income_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_house_score_without_house_should_do_nothing():
    profile = {
        "age": 35,
        "dependents": 1,
        "income": 201000,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_house_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_house_score_mortgaged_house_should_add_points():
    profile = {
        "age": 35,
        "dependents": 1,
        "income": 201000,
        "house": {"ownership_status": "mortgaged"},
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_house_score()

    assert score == {
        "auto": 0,
        "disability": 1,
        "home": 1,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_house_score_owned_house_should_do_nothing():
    profile = {
        "age": 35,
        "dependents": 1,
        "income": 201000,
        "marital_status": "married",
        "house": {"ownership_status": "owned"},
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_house_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_dependent_score_zero_dependents_should_do_nothing():
    profile = {
        "age": 35,
        "dependents": 0,
        "income": 201000,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_dependent_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_dependent_score_two_dependents_should_add_one():
    profile = {
        "age": 35,
        "dependents": 2,
        "income": 201000,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_dependent_score()

    assert score == {
        "auto": 0,
        "disability": 1,
        "home": 0,
        "life": 1
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_marital_status_score_married_should_change_score():
    profile = {
        "age": 35,
        "dependents": 2,
        "income": 201000,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_relationship_score()

    assert score == {
        "auto": 0,
        "disability": -1,
        "home": 0,
        "life": 1
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_marital_status_score_single_should_not_change_score():
    profile = {
        "age": 35,
        "dependents": 2,
        "income": 201000,
        "marital_status": "single",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_relationship_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_vehicle_status_score_without_vehicle_should_not_change_score():
    profile = {
        "age": 35,
        "dependents": 2,
        "income": 201000,
        "marital_status": "single",
        "risk_questions": [0, 1, 0],
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_vehicle_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_vehicle_status_score_old_vehicle_should_not_change_score():
    profile = {
        "age": 35,
        "dependents": 2,
        "income": 201000,
        "marital_status": "single",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 1990}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_vehicle_score()

    assert score == {
        "auto": 0,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_calculate_vehicle_status_score_new_vehicle_should_add_one_auto():
    profile = {
        "age": 35,
        "dependents": 2,
        "income": 201000,
        "marital_status": "single",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": datetime.now().year - 1}
    }

    rp_service = RiskProfileService(profile)
    score = rp_service.calculate_vehicle_score()

    assert score == {
        "auto": 1,
        "disability": 0,
        "home": 0,
        "life": 0
    }
    assert rp_service.risk_profile == {
        "auto": "economic",
        "disability": "economic",
        "home": "economic",
        "life": "economic"
    }


def test_set_risk_from_score_should_work_without_ineligible():
    rp_service = RiskProfileService(None)
    rp_service.score = {
        "auto": 3,
        "disability": 2,
        "home": 1,
        "life": 0
    }

    profile = rp_service.set_risk_from_score()
    assert profile == {
        "auto": "responsible",
        "disability": "regular",
        "home": "regular",
        "life": "economic"
    }


def test_set_risk_from_score_should_work_with_ineligible():
    rp_service = RiskProfileService(None)
    rp_service.score = {
        "auto": 3,
        "disability": 2,
        "home": 1,
        "life": 0
    }

    rp_service.risk_profile["life"] = "ineligible"

    profile = rp_service.set_risk_from_score()
    assert profile == {
        "auto": "responsible",
        "disability": "regular",
        "home": "regular",
        "life": "ineligible"
    }
