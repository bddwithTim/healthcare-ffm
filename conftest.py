import pytest
from datetime import datetime

from src.browser import get_driver
from pathlib import Path


@pytest.fixture(scope="session")
def driver():
    web_driver = get_driver(headless=False)
    yield web_driver
    web_driver.quit()


def pytest_cmdline_preparse(args):
    root_dir = Path(__file__).parent
    # generates an html report using the pytest-html plugin
    args.extend(
        ["--html", f'{root_dir}/reports/report_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.html']
    )
