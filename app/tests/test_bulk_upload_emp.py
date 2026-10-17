from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ---------------- /possible_fields --------------------
def test_possible_fields(test_db):
    response = client.get(
        "/possible_fields"
    )
    res = response.json()
    response.status_code == 200
    assert len(res["possible_fields"]) == 11


# ---------------- /employees_bulk_upload --------------------
data = {"lines":[
    {
        "first_name":{"value":"Nour","rowIndex":7,"colIndex":0},
        "last_name":{"value":"Chaabane","rowIndex":7,"colIndex":1},
        "email":{"value":"nourchaabane@example.com","rowIndex":7,"colIndex":2},
        "number":{"value":"321726","rowIndex":7,"colIndex":3},
        "birth_date":{"value":"1994-04-05","rowIndex":7,"colIndex":4},
        "address":{"value":"9 Rue de Palestine, Ariana","rowIndex":7,"colIndex":5},
        "cnss_number":{"value":"89012345-67","rowIndex":7,"colIndex":6},
        "contract_type":{"value":"CDD","rowIndex":7,"colIndex":7},
        "gender":{"value":"MALE","rowIndex":7,"colIndex":8},
        "phone_number":{"value":"27890123","rowIndex":7,"colIndex":9},
        "roles":{"value":"ADMIN","rowIndex":7,"colIndex":10}
    }],
    "force_uploade":False
}
def test_employees_bulk_upload(test_db):
    response = client.post(
        "/employees_bulk_upload",
        json = data
    )
    res = response.json()
    assert response.status_code == 200
    assert "errs" in res 
    assert "warnings" in res
    assert "detail" in res