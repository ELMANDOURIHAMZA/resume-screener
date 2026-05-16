import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
resp = client.post("/api/v1/rank", json={"job_description":"python developer","resumes":[],"top_k":3})
import json
print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
