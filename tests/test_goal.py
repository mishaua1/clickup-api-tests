import requests
import os
from dotenv import load_dotenv
from faker import Faker

load_dotenv(dotenv_path=".env")

fake = Faker()

TOKEN = os.getenv("TOKEN")
TEAM_ID = os.getenv("TEAM_ID")
BASE_URL = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

goal_id = None
original_name = fake.user_name()
updated_name = "Updated via PUT"

def test_create_goal():
    global goal_id
    body = {
        "name": original_name,
        "description": "Created by Python",
        "due_date": None
    }
    response = requests.post(f"{BASE_URL}/team/{TEAM_ID}/goal", headers=HEADERS, json=body)
    assert response.status_code == 200
    goal_id = response.json()["goal"]["id"]
    assert response.json()["goal"]["name"] == original_name

def test_get_goal_valid():
    response = requests.get(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["goal"]["name"] == original_name

def test_get_goal_invalid():
    response = requests.get(f"{BASE_URL}/goal/invalid_goal_id", headers=HEADERS)
    assert response.status_code in [404, 500]

def test_get_goal_no_token():
    response = requests.get(f"{BASE_URL}/goal/{goal_id}")
    assert response.status_code in [400, 401]

def test_update_goal():
    body = {"name": updated_name}
    response = requests.put(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS, json=body)
    assert response.status_code == 200

def test_get_updated_goal():
    response = requests.get(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["goal"]["name"] == updated_name

def test_delete_goal():
    response = requests.delete(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS)
    assert response.status_code == 200

def test_get_deleted_goal():
    response = requests.get(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS)
    assert response.status_code == 404
