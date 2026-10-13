from app.app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health():
    r = client().get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_version():
    r = client().get("/version")
    assert r.status_code == 200
    assert "version" in r.get_json()


def test_index():
    r = client().get("/")
    assert r.status_code == 200
    assert b"Deployed by Jenkins" in r.data


def test_unknown_route_returns_404():
    assert client().get("/does-not-exist").status_code == 404
