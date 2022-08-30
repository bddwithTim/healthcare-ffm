from typing import List

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class Browser:
    """
    Utility class for handling Browser operations.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.rest = WebDriverWait(self.driver, 30)

    def wait_for_element_to_be_clickable(self, element: str) -> WebElement:
        try:
            return self.rest.until(ec.element_to_be_clickable((By.XPATH, element)))
        except TimeoutException:
            assert False, f"web element '{element}' not found"

    def get_web_element(self, element: str) -> WebElement:
        return self.rest.until(ec.presence_of_element_located((By.XPATH, element)))

    def get_web_elements(self, element: str) -> List[WebElement]:
        return self.rest.until(ec.presence_of_all_elements_located((By.XPATH, element)))

    def click(self, element_value: str) -> None:
        web_element = self.wait_for_element_to_be_clickable(element_value)
        web_element.click()

    def navigate(self, url: str, clear_cookie: bool = True) -> None:
        """Open an absolute URL."""
        if clear_cookie:
            self.driver.delete_all_cookies()
            self.driver.refresh()
        self.driver.get(url)

    def close_subscription_dialog(self, timeout: int = 5) -> None:
        """
        Close subscription dialog that is displayed by default
        """
        subscription_dialog = "//button[text()='Close subscription dialog']"
        self.rest = WebDriverWait(self.driver, timeout)
        self.rest.until(ec.presence_of_element_located((By.XPATH, subscription_dialog)))
        self.click(subscription_dialog)

        # confirm that the subscription dialog is no longer attached to the DOM
        self.rest.until(ec.invisibility_of_element_located((By.XPATH, subscription_dialog)))

    def close_modal_dialog(self, timeout: int = 5) -> None:
        """
        Close `Help comparing plans` modal
        """
        modal_dialog = "//button[@aria-label='Close modal dialog']"
        self.rest = WebDriverWait(self.driver, timeout)
        self.rest.until(ec.presence_of_element_located((By.XPATH, modal_dialog)))
        self.click(modal_dialog)

        # confirm that the modal dialog is no longer attached to the DOM
        self.rest.until(ec.invisibility_of_element_located((By.XPATH, modal_dialog)))

    def scroll_into_view(self, element_value: str) -> None:
        web_element = self.wait_for_element_to_be_clickable(element_value)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)

    def click_next_pagination(self) -> None:
        self.scroll_into_view("//span[contains(text(),'Next')]")
        self.click("//span[contains(text(),'Next')]")

    def input_zip_code(self, zip_code: str, county: str) -> None:
        """
        Input correct zip-code format
        """
        if len(zip_code) != 5:
            raise Exception("Zip code must be 5 digits long")

        self.fill(data=zip_code, web_element="//input[@name='ZIP Code']")
        self.click(f"//li[text()='{county}']")
        self.click("//button[text()='Continue']")

    def fill(self, data: str, web_element: str) -> None:
        """
        Fill information in an input field
        """
        element = self.rest.until(ec.presence_of_element_located((By.XPATH, web_element)))
        element.send_keys(data)

    def extract_all_plans(self) -> List:
        """
        Extract the plans information from the page.
        """
        plan_info = []
        max_pagination = int(self.rest.until(
            ec.presence_of_element_located((
                By.XPATH,
                "//span[contains(@class, 'page-count')]")
            )).text)

        for initial_pagination in range(1, max_pagination + 1):
            plans = self.get_web_elements("//article[contains(@class, 'plan-card--health')]")

            for plan in plans:
                plan_name = plan.find_element(By.XPATH, ".//h2[contains(@class, 'pet-c-plan-title__name')]").text
                plan_provider = plan.find_element(By.XPATH, ".//div[contains(@class, 'plan-title__issuer')]").text
                plan_premium = plan.find_element(By.XPATH, ".//div[contains(@class, 'plan-summary__premium-with-credit')]").text

                plan_information = {'Plan name': plan_name, 'Provider': plan_provider, 'Monthly premium': plan_premium}
                plan_info.append(plan_information)

            # click Next page button
            if initial_pagination < max_pagination:
                self.click_next_pagination()

        return plan_info


def get_driver(headless: bool = False) -> webdriver:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")

    return webdriver.Chrome(executable_path=".\\src\\drivers\\chromedriver.exe", options=chrome_options)
