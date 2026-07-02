import os
import traceback
# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

try:
    response = client.post("/chat", json={
        "message": "I need to leave home, drop off my dry cleaning, grab some milk at the grocery store, and then head to the office before 9am."
    })
    print("Status:", response.status_code)
    print("Body:", response.json())
except Exception as e:
    print("Error during test:")
    traceback.print_exc()
