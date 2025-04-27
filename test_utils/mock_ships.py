
from fastapi.testclient import TestClient


def _create_mock_ships(client: TestClient, count: int) -> None:
    """
    Create mock ships for testing.
    """
    for i in range(count):
        client.post("/ships/", json={
            "name": f"Test Ship {i}",
            "classification": f"Test Classification {i}",
            "sign": f"Test Sign {i}",
            "speed": f"Test Speed {i}",
            "captain": f"Test Captain {i}",
            "comment": f"Test Comment {i}",
            "url": f"http://example.com/{i}"
        })
