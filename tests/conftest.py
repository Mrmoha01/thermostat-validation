import pytest

from dut import Dut
from thermostat.sim import Thermostat


def pytest_addoption(parser):
    parser.addoption("--fw", default="1.0.0", help="firmware version to test")


def pytest_report_header(config):
    return f"firmware under test: {config.getoption('--fw')}"


def pytest_collection_modifyitems(items):
    missing = [item.nodeid for item in items if not item.get_closest_marker("req")]
    if missing:
        raise pytest.UsageError(f"tests without a req marker: {missing}")


@pytest.fixture
def fw(request):
    return request.config.getoption("--fw")


@pytest.fixture
def sim(fw):
    return Thermostat(version=fw)


@pytest.fixture
def dut(sim):
    return Dut(sim)


# add a Requirement column to the pytest-html report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    outcome.get_result().req = item.get_closest_marker("req").args[0]


def pytest_html_results_table_header(cells):
    cells.insert(1, "<th>Requirement</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(1, f"<td>{getattr(report, 'req', '')}</td>")
