from flask import Response

def test_index_ok(client):
    response: Response = client.get("/")
    assert 200 == response.status_code
    assert b"<h1>Welcome!</h1><h2>API is at edpoint <b>/api/stt</b></h2>" == response.data


def test_index_unauthorised_method(client):
    res: Response = client.post("/")
    assert 405 == res.status_code