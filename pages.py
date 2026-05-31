# pages.py — Page Object Model para o Urban Routes (Sprint 8)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:

    # ── Localizadores: Campos de endereço ──
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # ── Localizadores: Botão para solicitar táxi ──
    call_a_taxi_button = (By.CSS_SELECTOR, 'button.button.round')

    # ── Localizadores: Tarifa Comfort ──
    comfort_tariff = (By.XPATH, '//div[contains(@class, "tcard-title") and text()="Comfort"]')
    comfort_tariff_active = (By.XPATH, '//div[contains(@class, "tcard") and contains(@class, "active")]//div[text()="Comfort"]')

    # ── Localizadores: Telefone ──
    phone_button = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    phone_next_button = (By.XPATH, '//form//button[@type="submit"]')
    sms_code_input = (By.ID, 'code')
    sms_confirm_button = (By.XPATH, '//div[contains(@class, "section")]//button[contains(text(), "Confirmar")]')

    # ── Localizadores: Cartão de crédito ──
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_link = (By.XPATH, '//div[contains(text(), "Adicionar cart")]')
    card_number_input = (By.ID, 'number')
    card_cvv_input = (By.CSS_SELECTOR, '.card-input#code')
    card_add_button = (By.XPATH, '//form[contains(@class, "card-wrapper")]//button[@type="submit"]')
    close_payment_modal = (By.XPATH, '//div[contains(@class, "payment-picker")]//button[contains(@class, "close-button")]')

    # ── Localizadores: Comentário para o motorista ──
    comment_input = (By.ID, 'comment')

    # ── Localizadores: Cobertor e lenços ──
    blanket_and_handkerchiefs_slider = (By.XPATH,
        '//div[contains(@class, "reqs")]//div[contains(@class, "r-sw")]//div[contains(@class, "switch")]')
    blanket_and_handkerchiefs_checkbox = (By.XPATH,
        '//div[contains(@class, "reqs")]//div[contains(@class, "r-sw")]//input[@type="checkbox"]')

    # ── Localizadores: Sorvete ──
    ice_cream_plus_button = (By.XPATH,
        '//div[contains(@class, "r-counter")]//div[contains(@class, "counter-plus")]')
    ice_cream_counter_value = (By.XPATH,
        '//div[contains(@class, "r-counter")]//div[contains(@class, "counter-value")]')

    # ── Localizadores: Botão de pedir táxi e modal de busca ──
    order_button = (By.CSS_SELECTOR, '.smart-button-main')
    order_modal_title = (By.CLASS_NAME, 'order-header-title')

    # ────────────────────────────────────────────
    # Construtor
    # ────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver

    # ────────────────────────────────────────────
    # Métodos auxiliares (esperas)
    # ────────────────────────────────────────────
    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    # ────────────────────────────────────────────
    # 1. Definir endereço (rota)
    # ────────────────────────────────────────────
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

    # ────────────────────────────────────────────
    # 2. Selecionar tarifa Comfort
    # ────────────────────────────────────────────
    def click_call_taxi_button(self):
        self.wait_for_clickable(self.call_a_taxi_button)
        self.driver.find_element(*self.call_a_taxi_button).click()

    def select_comfort_tariff(self):
        self.wait_for_clickable(self.comfort_tariff)
        # Verifica se a tarifa Comfort já está selecionada para evitar cliques desnecessários
        comfort_elements = self.driver.find_elements(*self.comfort_tariff_active)
        if len(comfort_elements) == 0:
            self.driver.find_element(*self.comfort_tariff).click()

    def is_comfort_selected(self):
        return len(self.driver.find_elements(*self.comfort_tariff_active)) > 0

    # ────────────────────────────────────────────
    # 3. Preencher número de telefone
    # ────────────────────────────────────────────
    def click_phone_button(self):
        self.wait_for_clickable(self.phone_button)
        self.driver.find_element(*self.phone_button).click()

    def set_phone_number(self, phone_number):
        self.wait_for_element(self.phone_input)
        self.driver.find_element(*self.phone_input).send_keys(phone_number)

    def click_phone_next_button(self):
        self.driver.find_element(*self.phone_next_button).click()

    def set_sms_code(self, code):
        self.wait_for_element(self.sms_code_input)
        self.driver.find_element(*self.sms_code_input).send_keys(code)

    def click_sms_confirm_button(self):
        self.driver.find_element(*self.sms_confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_button).text

    # ────────────────────────────────────────────
    # 4. Adicionar cartão de crédito
    # ────────────────────────────────────────────
    def click_payment_method(self):
        self.wait_for_clickable(self.payment_method_button)
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card(self):
        self.wait_for_clickable(self.add_card_link)
        self.driver.find_element(*self.add_card_link).click()

    def set_card_number(self, card_number):
        self.wait_for_element(self.card_number_input)
        self.driver.find_element(*self.card_number_input).send_keys(card_number)

    def set_card_cvv(self, cvv_code):
        self.wait_for_element(self.card_cvv_input)
        self.driver.find_element(*self.card_cvv_input).send_keys(cvv_code)
        # Retira o foco do campo CVV pressionando TAB (exigido para ativar o botão Adicionar)
        self.driver.find_element(*self.card_cvv_input).send_keys(Keys.TAB)

    def click_card_add_button(self):
        self.wait_for_clickable(self.card_add_button)
        self.driver.find_element(*self.card_add_button).click()

    def close_payment(self):
        self.wait_for_clickable(self.close_payment_modal)
        self.driver.find_element(*self.close_payment_modal).click()

    # ────────────────────────────────────────────
    # 5. Comentário para o motorista
    # ────────────────────────────────────────────
    def set_comment(self, message):
        self.wait_for_element(self.comment_input)
        self.driver.find_element(*self.comment_input).send_keys(message)

    def get_comment(self):
        return self.driver.find_element(*self.comment_input).get_attribute('value')

    # ────────────────────────────────────────────
    # 6. Pedir cobertor e lenços
    # ────────────────────────────────────────────
    def click_blanket_and_handkerchiefs(self):
        self.wait_for_clickable(self.blanket_and_handkerchiefs_slider)
        self.driver.find_element(*self.blanket_and_handkerchiefs_slider).click()

    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.driver.find_element(*self.blanket_and_handkerchiefs_checkbox)
        return checkbox.is_selected()

    # ────────────────────────────────────────────
    # 7. Pedir sorvetes (loop movido do main.py para cá)
    # ────────────────────────────────────────────
    def add_ice_cream(self, quantity=2):
        for i in range(quantity):
            self.wait_for_clickable(self.ice_cream_plus_button)
            self.driver.find_element(*self.ice_cream_plus_button).click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter_value).text

    # ────────────────────────────────────────────
    # 8. Pedir táxi e verificar modal de busca
    # ────────────────────────────────────────────
    def click_order_button(self):
        self.wait_for_clickable(self.order_button)
        self.driver.find_element(*self.order_button).click()

    def is_order_modal_displayed(self):
        self.wait_for_visible(self.order_modal_title)
        return self.driver.find_element(*self.order_modal_title).is_displayed()
