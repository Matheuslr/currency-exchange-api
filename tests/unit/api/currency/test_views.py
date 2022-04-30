def test_get_all_currencies_view(client):
    response = client.get("/api/currency/")
    result = response.json()

    assert response.status_code == 200
