def test_get_buku_tanpa_token(client):
    """Endpoint GET buku harus menolak request tanpa token JWT."""
    response = client.get("/api/buku")
    assert response.status_code == 401

def test_home_endpoint(client):
    """Endpoint root harus mengembalikan status success."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"