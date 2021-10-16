from http import HTTPStatus

import pytest
from api_requests.api import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
   return TestClient(app)
 

def test_healthcheck(client):
   response = client.get("/healthcheck")
   assert response.status_code == HTTPStatus.OK
   

def test_healthcheck_return_json(client):
   response = client.get("/healthcheck")
   assert response.headers["Content-Type"] == "application/json"


def test_quando_verificar_integridade_deve_conter_informacoes(client):
   response = client.get("/healthcheck")
   assert response.json() == {
      "status": "ok"
   }