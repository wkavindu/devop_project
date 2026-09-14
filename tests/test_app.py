def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"service": "opstrack", "status": "healthy"}


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json["database"] == "connected"


def test_create_and_view_incident(client):
    response = client.post("/incidents/new", data={
        "title": "API outage", "service": "payments", "description": "Requests time out",
        "severity": "Critical", "status": "Open",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"API outage" in response.data
    dashboard = client.get("/")
    assert b"payments" in dashboard.data


def test_rejects_invalid_incident(client):
    response = client.post("/incidents/new", data={
        "title": "", "service": "api", "description": "Failure",
        "severity": "High", "status": "Open",
    })
    assert response.status_code == 200
    assert b"required" in response.data


def test_ci_detects_failure():
    """Intentional temporary failure to demonstrate CI protection."""
    assert False, "Intentional CI failure demonstration"