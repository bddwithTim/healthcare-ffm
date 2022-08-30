import pytest

from src import generate_excel_result, read_xls
from src.browser import Browser


@pytest.mark.parametrize("zip_code, county", read_xls("zipcode.xlsx", sheet_name='data'))
def test_healthcare_basic_flow(driver, zip_code: str, county: str) -> None:
    browser = Browser(driver)
    browser.navigate("https://www.healthcare.gov/see-plans/#/")
    # Close the subscription dialog that is displayed by default
    browser.close_subscription_dialog()
    browser.input_zip_code(zip_code, county)

    browser.click("//button[contains(text(),'See Full-Price Plans')]")
    browser.close_modal_dialog()  # `Help comparing plans` modal

    # extract plan information listed in the page
    data = browser.extract_all_plans()
    generate_excel_result(data, zip_code)