import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def approved_card():
    return {
        "number": "4444 4444 4444 4441",
        "month": "12",
        "year": "26",
        "owner": "Ivanov Ivan",
        "cvc": "123"
    }

@pytest.fixture
def declined_card():
    return {
        "number": "4444 4444 4444 4442",
        "month": "12",
        "year": "26",
        "owner": "Ivanov Ivan",
        "cvc": "123"
    }