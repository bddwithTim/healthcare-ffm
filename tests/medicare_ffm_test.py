import time
import pytest

from src import generate_medicare_result, read_xls
from src.browser import Browser


@pytest.mark.medicare
@pytest.mark.parametrize("zip_code, county_selection", read_xls("medicare_zipcode.xlsx", sheet_name='data'))
def test_healthcare_basic_flow(driver, zip_code: str, county_selection: str) -> None:
    browser = Browser(driver)
    browser.navigate("https://www.medicare.gov/")

    #close subscription dialog
    browser.click("//button[contains(text(), 'Close subscription dialog')]")

    browser.click("//a[contains(text(),'Preview 2023 Plans')]")
    browser.fill(zip_code,"//input[@name='zipcode']")

    browser.click("//span[contains(text(),'Select a plan type')]")
    time.sleep(0.8)
    browser.click("//input[@value='MEDICARE_ADVANTAGE_PLAN']")
    browser.click("//button[contains(text(),'Apply')]")

    # if state needs county selection
    browser.county_selection(county_selection)
    browser.click("//button[contains(text(),'Start')]")

    # wait for the page to be navigated and have a relative url
    browser.wait_for_url("year=2023&lang=en")
    browser.click("""//span[contains(text(),"I'm not sure")]""") # select "I'm not sure"
    browser.click("//button[contains(text(),'Continue Without Logging In')]")

    # wait for the page to be navigated and have a relative url
    browser.wait_for_url("fips=")
    # Do you want to see your drug costs when you compare plans?
    browser.click("//label//span[contains(text(), 'No')]")
    browser.click("//button[contains(text(),'Next')]")

    # wait for the plans list
    browser.wait_for_url("search-results?plan_type=")

    # extract medicare plans
    data = browser.extract_medicare_plans()
    generate_medicare_result(data, zip_code)

