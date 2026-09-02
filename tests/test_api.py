import os
os.environ['DATABASE_URL'] = 'sqlite:///./test_pytest.db'

from fastapi.testclient import TestClient
from app.main import app
from app.database.session import init_db

init_db()
client = TestClient(app)


def test_register_and_heartbeat():
    r = client.post('/services', json={'service_id':'tservice','name':'T Service'})
    assert r.status_code in (200,201)
    r = client.post('/heartbeat', json={'service_id':'tservice','latency_ms':5})
    assert r.status_code in (200,201)
    r = client.get('/services/tservice')
    assert r.status_code == 200
    data = r.json()
    assert data['service_id'] == 'tservice'
    assert data['status'] == 'online'


def test_metrics_latency():
    # create several heartbeats
    for v in [10,20,30]:
        client.post('/heartbeat', json={'service_id':'metric-svc','latency_ms':v})
    r = client.get('/services/metric-svc/metrics')
    assert r.status_code == 200
    data = r.json()
    assert data['min_ms'] == 10
    assert data['max_ms'] == 30
    assert abs(data['avg_ms'] - 20.0) < 0.001
