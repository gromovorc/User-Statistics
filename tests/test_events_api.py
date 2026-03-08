import os
import subprocess
import pytest
import sqlalchemy as sa

from datetime import datetime, timezone, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from app.db.models.events import events_table
from app.main import app
from app.db.database import get_connection
from app.schemas.event import EventCreate

TEST_DB_URL = "postgresql+psycopg2://admin:secret@localhost:5433/postgres_db_test"

@pytest.fixture(scope="session")
def test_engine():
    engine = sa.create_engine(TEST_DB_URL, pool_pre_ping=True)
    return engine

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    env = os.environ.copy()
    env["DATABASE_URL"] = TEST_DB_URL
    subprocess.check_call(
        ["python", "-m", "alembic", "upgrade", "head"],
        env=env,
        cwd="S:\\Work\\Projects\\User-Statistics"
    )

@pytest.fixture()
def client(test_engine):
    def override_get_connection():
        with test_engine.connect() as conn:
            yield conn

    app.dependency_overrides[get_connection] = override_get_connection

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clean_db(test_engine):
    with test_engine.begin() as conn:
        conn.execute(sa.text("TRUNCATE TABLE events RESTART IDENTITY"))



def test_events_conflict(client: TestClient, test_engine):
    dummy_event_id = '00000000-0000-0000-0000-000000000001'
    dummy_event_time = datetime(year=2024, month=1, day=1, hour=12, tzinfo=timezone.utc)
    dummy_user_id = 999


    payload = EventCreate(
        event_id = dummy_event_id,
        event_time = dummy_event_time.isoformat(),
        event_type =  "click",
        user_id = dummy_user_id,
        properties = {}
    )
    _response = client.post("/events", json=jsonable_encoder(payload))

    select_stmt = (
        sa.select(
            sa.func.count()
        )
        .select_from(events_table).where(events_table.c.event_id == dummy_event_id)
    )

    with test_engine.connect() as _connection:
        rows = _connection.execute(select_stmt).scalar()

    assert _response.status_code == 201
    assert rows == 1

    _response = client.post("/events", json=jsonable_encoder(payload))

    with test_engine.connect() as _connection:
        rows = _connection.execute(select_stmt).scalar()

    assert _response.status_code == 200
    assert rows == 1

    conflict_payload = payload.model_dump()
    conflict_payload["event_type"] = "buy"

    _response = client.post("/events", json=jsonable_encoder(conflict_payload))

    with test_engine.connect() as _connection:
        rows = _connection.execute(select_stmt).scalar()

    assert _response.status_code == 409
    assert rows == 1

def test_list_user_events(client: TestClient, test_engine):
    payload_with_users = list()
    dummy_event_time = datetime(year=2024, month=1, day=1, hour=12, tzinfo=timezone.utc)

    for i in range(3):
        payload_with_users.append(
            EventCreate(
                event_id=uuid4(),
                event_time=(dummy_event_time + timedelta(hours=i)).isoformat(),
                event_type=f"click{i}",
                user_id=1,
                properties={}
            )
        )

    payload_with_users.append(
        EventCreate(
            event_id=uuid4(),
            event_time=(dummy_event_time + timedelta(hours=3)).isoformat(),
            event_type="buy",
            user_id=2,
            properties={}
        )
    )

    for event in payload_with_users:
        client.post("/events", json=jsonable_encoder(event))

    _response = client.get("/users/1/events")
    _data = _response.json()

    assert _response.status_code == 200
    assert _data[0]["user_id"] == 1
    assert len(_data) == 3
    assert _data[0]["event_time"] >= _data[-1]["event_time"]

    _response = client.get("/users/1/events?limit=1&offset=1")
    _data = _response.json()

    assert _response.status_code == 200
    assert _data[0]["user_id"] == 1
    assert len(_data) == 1
    assert _data[0]["event_type"] == "click1"

    _response = client.get("/users/2/events?event_type=buy")
    _data = _response.json()

    assert _response.status_code == 200
    assert _data[0]["user_id"] == 2
    assert len(_data) == 1
    assert _data[0]["event_type"] == "buy"


