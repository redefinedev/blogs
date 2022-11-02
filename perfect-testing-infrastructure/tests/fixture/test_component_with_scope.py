import pytest
import docker
import requests
from tests.utils.test_utils import wait_for_server


@pytest.fixture(scope="module")
def web():
    port = 80

    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server2/", tag="web_server2")
    container = client.containers.run(
        image="web_server2", auto_remove=True, detach=True, network_mode="host"
    )

    wait_for_server(port)

    yield {"port": port}

    # Teardown
    container.kill()


def test_odd_sanity(web):
    # Execute
    response_odd = requests.get(f"http://127.0.0.1:{web['port']}/is_odd?number=1")

    # Assert
    assert response_odd.status_code == 200
    assert response_odd.json() == True


def test_odd_even(web):
    # Execute
    response_even = requests.get(f"http://127.0.0.1:{web['port']}/is_odd?number=2")

    # Assert
    assert response_even.status_code == 200
    assert response_even.json() == False


def test_odd_zero(web):
    # Execute
    response_zero = requests.get(f"http://127.0.0.1:{web['port']}/is_odd?number=0")

    # Assert
    assert response_zero.status_code == 200
    assert response_zero.json() == False


@pytest.mark.xfail
def test_odd_sanity_fail(web):
    # Execute
    response_odd = requests.get(f"http://127.0.0.1:{web['port']}/is_odd?number=1")

    # Assert
    assert response_odd.status_code == 200
    assert response_odd.json() == False
