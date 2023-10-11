def test_index(client):
    response = client.get("/")
    assert 200 == response.status_code
    assert b"<h1>Welcome!</h1><h2>API is at edpoint <b>/api/stt</b></h2>" in response.data
