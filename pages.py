import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_a_taxi_button = (By.CSS_SELECTOR, 'button.button.round')
    comfort_tariff = (By.XPATH, '//div[contains(@class,"tcard-title") and text()="Comfort"]')
    comfort_tariff_active = (By.XPATH, '//div[contains(@class,"tcard") and contains(@class,"active")]//div[text()="Comfort"]')
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    phone_next_button = (By.CSS_SELECTOR, '.section.active .buttons button[type="submit"]')
    sms_code_input = (By.ID, 'code')
    sms_confirm_button = (By.CSS_SELECTOR, '.section.active .buttons button[type="submit"]')
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_link = (By.CSS_SELECTOR, '.pp-plus-container')
    card_number_input = (By.XPATH, '//div[contains(@class,"card-wrapper")]//input[@id="number"]')
    card_cvv_input = (By.XPATH, '//div[contains(@class,"card-wrapper")]//input[@id="code"]')
    card_add_button = (By.CSS_SELECTOR, '.pp-buttons button[type="submit"]')
    close_payment_modal = (By.XPATH, '//div[contains(@class,"payment-picker")]//button[contains(@class,"close-button")]')
    comment_input = (By.ID, 'comment')
    blanket_and_handkerchiefs_slider = (By.XPATH, '//div[contains(@class,"r-sw")]//div[contains(@class,"switch")]')
    blanket_and_handkerchiefs_checkbox = (By.XPATH, '//div[contains(@class,"r-sw")]//input[@type="checkbox"]')
    ice_cream_plus_button = (By.XPATH, '//div[contains(@class,"r-counter")]//div[contains(@class,"counter-plus")]')
    ice_cream_counter_value = (By.XPATH, '//div[contains(@class,"r-counter")]//div[contains(@class,"counter-value")]')
    order_button = (By.CSS_SELECTOR, '.smart-button-main')
    order_modal_title = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_visible(self, locator, timeout=20):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)

    def js_click(self, locator):
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def set_from(self, address):
        self.wait_for_element(self.from_field)
        self.driver.find_element(*self.from_field).send_keys(address)

    def set_to(self, address):
        self.wait_for_element(self.to_field)
        self.driver.find_element(*self.to_field).send_keys(address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_attribute('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_attribute('value')

    def click_call_taxi_button(self):
        self.wait_for_clickable(self.call_a_taxi_button)
        self.driver.find_element(*self.call_a_taxi_button).click()

    def select_comfort_tariff(self):
        self.wait_for_clickable(self.comfort_tariff)
        if len(self.driver.find_elements(*self.comfort_tariff_active)) == 0:
            self.driver.find_element(*self.comfort_tariff).click()

    def is_comfort_selected(self):
        return len(self.driver.find_elements(*self.comfort_tariff_active)) > 0

    def click_phone_button(self):
        self.wait_for_clickable(self.phone_button)
        self.driver.find_element(*self.phone_button).click()

    def set_phone_number(self, phone_number):
        self.wait_for_visible(self.phone_input)
        self.driver.find_element(*self.phone_input).send_keys(phone_number)

    def click_phone_next_button(self):
        self.wait_for_clickable(self.phone_next_button)
        self.driver.find_element(*self.phone_next_button).click()

    def set_sms_code(self, code):
        self.wait_for_visible(self.sms_code_input)
        self.driver.find_element(*self.sms_code_input).send_keys(code)

    def click_sms_confirm_button(self):
        self.wait_for_clickable(self.sms_confirm_button)
        self.driver.find_element(*self.sms_confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_button).text

    def click_payment_method(self):
        self.wait_for_clickable(self.payment_method_button)
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card(self):
        add_card = self.wait_for_clickable(self.add_card_link)
        self.driver.execute_script("arguments[0].click();", add_card)

    def set_card_number(self, card_number):
        self.wait_for_visible(self.card_number_input)
        self.driver.find_element(*self.card_number_input).send_keys(card_number)

    def set_card_cvv(self, cvv_code):
        cvv = self.wait_for_visible(self.card_cvv_input)
        cvv.send_keys(cvv_code)
        cvv.send_keys(Keys.TAB)

    def click_card_add_button(self):
        add_button = self.wait_for_clickable(self.card_add_button)
        self.driver.execute_script("arguments[0].click();", add_button)

    def close_payment(self):
        try:
            self.wait_for_clickable(self.close_payment_modal, timeout=5)
            self.driver.find_element(*self.close_payment_modal).click()
        except Exception:
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

    def set_comment(self, message):
        comment = self.wait_for_element(self.comment_input)
        self.scroll_to(comment)
        comment.send_keys(message)

    def get_comment(self):
        return self.driver.find_element(*self.comment_input).get_attribute('value')

    def click_blanket_and_handkerchiefs(self):
        slider = self.wait_for_element(self.blanket_and_handkerchiefs_slider)
        self.scroll_to(slider)
        self.driver.execute_script("arguments[0].click();", slider)

    def is_blanket_and_handkerchiefs_selected(self):
        return self.driver.find_element(*self.blanket_and_handkerchiefs_checkbox).is_selected()

    def add_ice_cream(self, quantity=2):
        btn = self.wait_for_element(self.ice_cream_plus_button)
        self.scroll_to(btn)
        for i in range(quantity):
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*self.ice_cream_plus_button))

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter_value).text

    def click_order_button(self):
        btn = self.wait_for_element(self.order_button)
        self.scroll_to(btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_order_modal_displayed(self):
        self.wait_for_visible(self.order_modal_title, timeout=30)
        return self.driver.find_element(*self.order_modal_title).is_displayed()
