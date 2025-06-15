import pytest


@pytest.mark.integration
def test_normalize_address(client):
    response = client.get("/normalize_address/", params={"address": "user input"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "result": "address value"}


@pytest.mark.integration
def test_normalize_address_fail(client):
    response = client.get("/normalize_address/", params={"address": "a" * 60})
    assert response.status_code == 400
    assert response.json() == {"detail": "Превышена длина входного запроса"}
