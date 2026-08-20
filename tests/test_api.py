"""Integration tests for the /calculate REST endpoint."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_calculate_happy_path():
    response = client.post("/calculate", json={"expression": "3 4 +"})
    assert response.status_code == 200
    assert response.json() == {"result": 7}


def test_calculate_precedence_via_rpn():
    response = client.post("/calculate", json={"expression": "3 4 + 2 *"})
    assert response.status_code == 200
    assert response.json() == {"result": 14}


def test_calculate_all_operators_smoke():
    cases = [
        ("2 3 +", 5),
        ("5 3 -", 2),
        ("4 5 *", 20),
        ("10 2 /", 5),
        ("2 8 ^", 256),
        ("9 sqrt", 3),
    ]
    for expression, expected in cases:
        response = client.post("/calculate", json={"expression": expression})
        assert response.status_code == 200
        assert response.json() == {"result": expected}


def test_calculate_error_stack_underflow():
    response = client.post("/calculate", json={"expression": "1 +"})
    assert response.status_code == 400
    assert "stack underflow" in response.json()["error"]


def test_calculate_error_division_by_zero():
    response = client.post("/calculate", json={"expression": "1 0 /"})
    assert response.status_code == 400
    assert "division by zero" in response.json()["error"]


def test_calculate_error_unknown_operator():
    response = client.post("/calculate", json={"expression": "1 2 %"})
    assert response.status_code == 400
    assert "invalid token" in response.json()["error"]


def test_calculate_error_non_numeric_token():
    response = client.post("/calculate", json={"expression": "foo bar +"})
    assert response.status_code == 400
    assert "invalid token" in response.json()["error"]
