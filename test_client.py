import os
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('GET /health =>', client.get('/health').status_code, client.get('/health').json())

r = client.post('/services', json={'service_id':'service-a','name':'Service A'})
print('POST /services =>', r.status_code, r.json())

print('GET /services =>', client.get('/services').status_code, client.get('/services').json())

r2 = client.post('/heartbeat', json={'service_id':'service-a','latency_ms':25})
print('POST /heartbeat =>', r2.status_code, r2.json())

print('GET /services/service-a =>', client.get('/services/service-a').status_code, client.get('/services/service-a').json())
