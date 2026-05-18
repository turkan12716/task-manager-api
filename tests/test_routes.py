import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "TASKS": [],        # Hər test üçün təmiz data mühiti
        "TASK_COUNTER": 0
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# --- Test 1: Web UI Əsas Səhifə Testi ---
def test_web_ui(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Task Manager API UI" in r.data

# --- Test 2: Health Endpoint Testi ---
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

# --- Test 3: Info Endpoint Versiya Testi ---
def test_info_contains_version(client):
    r = client.get("/info")
    data = r.get_json()
    assert r.status_code == 200
    assert "version" in data
    assert data["version"] == "1.0.0"

# --- Test 4: Task Yaradılması Testi ---
def test_create_task(client):
    r = client.post("/tasks", json={"title": "Buy milk", "description": "2 litres"})
    assert r.status_code == 201
    data = r.get_json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "2 litres"
    assert data["id"] == 1
    assert data["done"] is False

# --- Test 5: Boş Başlıqla Task Yaradılma Xətası (400) ---
def test_create_task_validation_error(client):
    r = client.post("/tasks", json={"description": "No title here"})
    assert r.status_code == 400
    assert "error" in r.get_json()

# --- Test 6: Bütün Taskların Siyahısını Çəkmək ---
def test_get_all_tasks(client):
    # Öncə bir task əlavə edək
    client.post("/tasks", json={"title": "Task-1"})
    
    r = client.get("/tasks")
    assert r.status_code == 200
    data = r.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Task-1"

# --- Test 7: ID-yə görə Tək bir Taskı Çəkmək ---
def test_get_single_task(client):
    client.post("/tasks", json={"title": "Specific Task"})
    
    r = client.get("/tasks/1")
    assert r.status_code == 200
    assert r.get_json()["title"] == "Specific Task"

# --- Test 8: Tapşırığı Tamamlandı (PATCH) Etmək ---
def test_patch_task(client):
    client.post("/tasks", json={"title": "Incomplete Task"})
    
    r = client.get("/tasks/1")
    assert r.get_json()["done"] is False
    
    # Statusu dəyişək
    patch_r = client.patch("/tasks/1", json={"done": True})
    assert patch_r.status_code == 200
    assert patch_r.get_json()["done"] is True

# --- Test 9: Taskın Silinməsi (DELETE) Testi ---
def test_delete_task(client):
    client.post("/tasks", json={"title": "To Be Deleted"})
    
    delete_r = client.delete("/tasks/1")
    assert delete_r.status_code == 200
    
    # Silindikdən sonra tapılmamalıdır
    get_r = client.get("/tasks/1")
    assert get_r.status_code == 404
