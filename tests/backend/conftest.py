import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    # Snapshot/restore the in-memory activities store so tests don't leak state
    original_state = copy.deepcopy(activities)
    yield TestClient(app)
    activities.clear()
    activities.update(original_state)
