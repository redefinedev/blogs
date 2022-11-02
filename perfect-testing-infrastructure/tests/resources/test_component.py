from time import sleep
import pytest
import docker
import requests
from tests.utils.test_utils import wait_for_server


@pytest.fixture(scope="module")
def web1(unused_tcp_port_factory):
    port = unused_tcp_port_factory()

    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server1/", tag="web_server1")
    container = client.containers.run(
        image="web_server1",
        auto_remove=True,
        detach=True,
        network_mode="bridge",
        ports={"80/tcp": f"{port}/tcp"},
    )

    wait_for_server(port)

    yield {"port": port}

    # Teardown
    container.kill()


@pytest.fixture(scope="module")
def web2(unused_tcp_port_factory):
    port = unused_tcp_port_factory()

    # Setup
    client = docker.from_env()
    client.images.build(path="pti/web_server2/", tag="web_server2")
    container = client.containers.run(
        image="web_server2",
        auto_remove=True,
        detach=True,
        network_mode="bridge",
        ports={"80/tcp": f"{port}/tcp"},
    )

    wait_for_server(port)

    yield {"port": port}

    # Teardown
    container.kill()


def test_both_servers(web1, web2):
    # Execute
    response_root = requests.get(f"http://127.0.0.1:{web1['port']}/")
    response_odd = requests.get(f"http://127.0.0.1:{web2['port']}/is_odd?number=1")
    # Assert
    assert response_root.status_code == 200
    assert response_root.json() == {"message": "Hello World"}
    assert response_odd.status_code == 200
    assert response_odd.json() == True
