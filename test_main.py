from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_upcoming_transactions():
    response = client.get("/transactions/upcoming")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_avg():
    response = client.get("/transactions/avg")
    assert response.status_code == 200
    assert response.json()


def test_transactions_month():
    response = client.get("/transactions/month")
    assert response.status_code == 200
    assert len(response.json()) > 0


# 1_TD-DS-1-0189758975-TD-TX-UpOp-7829404736
def test_transaction():
    response = client.get(
            "/transaction/1_TD-DS-1-0189758975-TD-TX-UpOp-7829404736")
    assert response.status_code == 200
    assert len(response.json()) > 0
