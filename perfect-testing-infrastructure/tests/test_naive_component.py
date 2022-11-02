import docker
import requests
from test_utils import wait_for_port


def test_root():
    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server1/", tag="web_server1")
    container = client.containers.run(
        image="web_server1", auto_remove=True, detach=True, network_mode="host"
    )

    wait_for_port(80)

    # Execute
    response = requests.get("http://127.0.0.1/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

    # Teardown
    container.kill()


def test_odd_all():
    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server2/", tag="web_server2")
    container = client.containers.run(
        image="web_server2", auto_remove=True, detach=True, network_mode="host"
    )

    wait_for_port(80)

    # Execute
    response_odd = requests.get("http://127.0.0.1/is_odd?number=1")
    response_even = requests.get("http://127.0.0.1/is_odd?number=2")
    response_zero = requests.get("http://127.0.0.1/is_odd?number=0")

    # Assert
    assert response_odd.status_code == 200
    assert response_odd.json() == True
    assert response_even.status_code == 200
    assert response_even.json() == False
    assert response_zero.status_code == 200
    assert response_zero.json() == False

    # Teardown
    container.kill()


def test_odd_sanity():
    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server2/", tag="web_server2")
    container = client.containers.run(
        image="web_server2", auto_remove=True, detach=True, network_mode="host"
    )

    wait_for_port(80)

    # Execute
    response_odd = requests.get("http://127.0.0.1/is_odd?number=1")

    # Assert
    assert response_odd.status_code == 200
    assert response_odd.json() == True

    # Teardown
    container.kill()


def test_odd_even():
    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server2/", tag="web_server2")
    container = client.containers.run(
        image="web_server2", auto_remove=True, detach=True, network_mode="host"
    )

    wait_for_port(80)

    # Execute
    response_even = requests.get("http://127.0.0.1/is_odd?number=2")

    # Assert
    assert response_even.status_code == 200
    assert response_even.json() == False

    # Teardown
    container.kill()


def test_odd_zero():
    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server2/", tag="web_server2")
    container = client.containers.run(
        image="web_server2", auto_remove=True, detach=True, network_mode="host"
    )

    wait_for_port(80)

    # Execute
    response_zero = requests.get("http://127.0.0.1/is_odd?number=0")

    # Assert
    assert response_zero.status_code == 200
    assert response_zero.json() == False

    # Teardown
    container.kill()
