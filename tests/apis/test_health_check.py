def test_health_check(tst):
    response = tst.client.get("/health_check/")
    r_json = response.json
    assert response.status_code == 200, r_json
    assert r_json == {"message": "Hello World"}
