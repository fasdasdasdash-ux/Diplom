import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from pages.payment_page import PaymentPage

API_URL = "http://localhost:8080/api/v1/pay"

@allure.feature("Оплата тура")
class TestPayment:

    @allure.title("Успешная оплата по дебетовой карте (APPROVED)")
    def test_successful_debit_payment(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 4441", "12", "26", "Ivanov Ivan", "123")
        page.click_submit()
        
        response = requests.post(API_URL, json={
            "number": "4444 4444 4444 4441",
            "month": "12",
            "year": "26",
            "owner": "Ivanov Ivan",
            "cvc": "123"
        })
        assert response.json()["status"] == "APPROVED"

    @allure.title("Отказ при оплате по дебетовой карте (DECLINED)")
    def test_declined_debit_payment(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 4442", "12", "26", "Ivanov Ivan", "123")
        page.click_submit()
        
        response = requests.post(API_URL, json={
            "number": "4444 4444 4444 4442",
            "month": "12",
            "year": "26",
            "owner": "Ivanov Ivan",
            "cvc": "123"
        })
        assert response.json()["status"] == "DECLINED"

    @allure.title("Успешная оплата в кредит (APPROVED)")
    def test_successful_credit_payment(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить в кредит']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 4441", "12", "26", "Ivanov Ivan", "123")
        page.click_submit()
        
        response = requests.post(API_URL, json={
            "number": "4444 4444 4444 4441",
            "month": "12",
            "year": "26",
            "owner": "Ivanov Ivan",
            "cvc": "123"
        })
        assert response.json()["status"] == "APPROVED"

    @allure.title("Отказ при оплате в кредит (DECLINED)")
    def test_declined_credit_payment(self, driver):
        driver.get("http://localhost:8080")
        driver.find_element(By.XPATH, "//span[text()='Купить в кредит']").click()
        page = PaymentPage(driver)
        page.fill_card_data("4444 4444 4444 4442", "12", "26", "Ivanov Ivan", "123")
        page.click_submit()
        
        response = requests.post(API_URL, json={
            "number": "4444 4444 4444 4442",
            "month": "12",
            "year": "26",
            "owner": "Ivanov Ivan",
            "cvc": "123"
        })
        assert response.json()["status"] == "DECLINED"