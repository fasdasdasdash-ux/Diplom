import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.payment_page import PaymentPage

API_URL = "http://localhost:8080/api/v1/pay"

@allure.feature("Оплата тура")
class TestPayment:

    @allure.title("Успешная оплата по дебетовой карте (APPROVED)")
    def test_successful_debit_payment(self, driver, approved_card):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data(
            approved_card["number"],
            approved_card["month"],
            approved_card["year"],
            approved_card["owner"],
            approved_card["cvc"]
        )
        page.click_submit()

        with allure.step("Проверка API: статус APPROVED"):
            response = requests.post(API_URL, json=approved_card)
            assert response.json()["status"] == "APPROVED"

        with allure.step("Проверка UI: уведомление об успехе"):
            success = page.get_success_message()
            assert success.is_displayed()
            assert "Успешно" in success.text

    @allure.title("Отказ при оплате по дебетовой карте (DECLINED)")
    def test_declined_debit_payment(self, driver, declined_card):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data(
            declined_card["number"],
            declined_card["month"],
            declined_card["year"],
            declined_card["owner"],
            declined_card["cvc"]
        )
        page.click_submit()

        with allure.step("Проверка API: статус DECLINED"):
            response = requests.post(API_URL, json=declined_card)
            assert response.json()["status"] == "DECLINED"

        with allure.step("Проверка UI: уведомление об ошибке"):
            error = page.get_error_message()
            assert error.is_displayed()
            assert "Ошибка" in error.text

    @allure.title("Успешная оплата в кредит (APPROVED)")
    def test_successful_credit_payment(self, driver, approved_card):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить в кредит']").click()
        page = PaymentPage(driver)
        page.fill_card_data(
            approved_card["number"],
            approved_card["month"],
            approved_card["year"],
            approved_card["owner"],
            approved_card["cvc"]
        )
        page.click_submit()

        with allure.step("Проверка API: статус APPROVED"):
            response = requests.post(API_URL, json=approved_card)
            assert response.json()["status"] == "APPROVED"

        with allure.step("Проверка UI: уведомление об успехе"):
            success = page.get_success_message()
            assert success.is_displayed()
            assert "Успешно" in success.text

    @allure.title("Отказ при оплате в кредит (DECLINED)")
    def test_declined_credit_payment(self, driver, declined_card):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить в кредит']").click()
        page = PaymentPage(driver)
        page.fill_card_data(
            declined_card["number"],
            declined_card["month"],
            declined_card["year"],
            declined_card["owner"],
            declined_card["cvc"]
        )
        page.click_submit()

        with allure.step("Проверка API: статус DECLINED"):
            response = requests.post(API_URL, json=declined_card)
            assert response.json()["status"] == "DECLINED"

        with allure.step("Проверка UI: уведомление об ошибке"):
            error = page.get_error_message()
            assert error.is_displayed()
            assert "Ошибка" in error.text

    @allure.title("Отказ при оплате с пустыми полями формы")
    def test_empty_fields(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.click_submit()

        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".input__sub"))
        )
        assert error.is_displayed()

    @allure.title("Отказ при оплате с неполным номером карты")
    def test_incomplete_card_number(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 444", "12", "26", "Ivanov Ivan", "123")
        page.click_submit()

        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Неверный формат']"))
        )
        assert error.is_displayed()

    @allure.title("Отказ при оплате просроченной картой (год)")
    def test_expired_year(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 4442", "12", "20", "Ivanov Ivan", "123")
        page.click_submit()

        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Истёк срок действия карты']"))
        )
        assert error.is_displayed()

    @allure.title("Отказ при оплате просроченной картой (месяц)")
    def test_expired_month(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 4442", "01", "26", "Ivanov Ivan", "123")
        page.click_submit()

        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='Неверно указан срок действия карты']"))
        )
        assert error.is_displayed()