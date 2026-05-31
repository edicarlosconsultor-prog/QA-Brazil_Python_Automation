import time
from selenium import webdriver
import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes.")
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.implicitly_wait(5)

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        time.sleep(3)
        helpers.retrieve_phone_code(self.driver)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from() == data.ADDRESS_FROM
        assert routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_call_taxi_button()
        routes_page.select_comfort_tariff()
        assert routes_page.is_comfort_selected()

    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_button()
        routes_page.set_phone_number(data.PHONE_NUMBER)
        routes_page.click_phone_next_button()
        time.sleep(2)
        sms_code = helpers.get_phone_code(self.driver)
        routes_page.set_sms_code(sms_code)
        routes_page.click_sms_confirm_button()
        time.sleep(1)
        assert data.PHONE_NUMBER in routes_page.get_phone_number()

    def test_fill_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card_number(data.CARD_NUMBER)
        routes_page.set_card_cvv(data.CARD_CODE)
        routes_page.click_card_add_button()
        routes_page.close_payment()
        time.sleep(1)
        pp_text = self.driver.find_element(*routes_page.payment_method_button).text
        assert len(pp_text) > 0

    def test_comment_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_comment(data.MESSAGE_FOR_DRIVER)
        assert routes_page.get_comment() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.js_click(routes_page.blanket_and_handkerchiefs_slider)
        assert routes_page.is_blanket_and_handkerchiefs_selected()

    def test_order_2_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream(2)
        assert routes_page.get_ice_cream_count() == '2'

    def test_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.js_click(routes_page.order_button)
        assert routes_page.is_order_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()