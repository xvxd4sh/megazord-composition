"""pytest plugin configuration.

https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
"""
# Third-Party Libraries
import pytest


@pytest.fixture(scope="session")
def apache_container(dockerc):
    """Return the apache container from the Docker composition."""
    # find the container by name even if it is stopped already"
    return dockerc.containers(service_names=["apache"], stopped=True)[0]


@pytest.fixture(scope="session")
def coredns_container(dockerc):
    """Return the coredns container from the Docker composition."""
    # find the container by name even if it is stopped already
    return dockerc.containers(service_names=["coredns"], stopped=True)[0]


@pytest.fixture(scope="session")
def cobalt_container(dockerc):
    """Return the cobalt strike container from the Docker composition."""
    # find the container by name even if it is stopped already
    return dockerc.containers(service_names=["cobalt"], stopped=True)[0]


def pytest_addoption(parser):
    """Add new commandline options to pytest."""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify collected tests based on custom marks and commandline options."""
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
