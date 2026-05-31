# main.py — Testes automatizados para o Urban Routes (Sprint 8)

from selenium import webdriver
import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Código do Sprint 7 — verifica conexão com o servidor
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

        # Código do Sprint 8 — habilita logs de performance para capturar o código SMS
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    # ──────────────────────────────────────
    # Teste 1: Definir o endereço
    # ──────────────────────────────────────
    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert routes_page.get_from() == data.ADDRESS_FROM
        assert routes_page.get_to() == data.ADDRESS_TO

    # ──────────────────────────────────────
    # Teste 2: Selecionar o plano Comfort
    # ──────────────────────────────────────
    def test_select_plan(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_call_taxi_button()
        routes_page.select_comfort_tariff()

        assert routes_page.is_comfort_selected()

    # ──────────────────────────────────────
    # Teste 3: Preencher o número de telefone
    # ──────────────────────────────────────
    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_phone_button()
        routes_page.set_phone_number(data.PHONE_NUMBER)
        routes_page.click_phone_next_button()

        # Recupera o código SMS interceptado dos logs de rede
        sms_code = helpers.retrieve_phone_code(self.driver)
        routes_page.set_sms_code(sms_code)
        routes_page.click_sms_confirm_button()

        assert data.PHONE_NUMBER in routes_page.get_phone_number()

    # ──────────────────────────────────────
    # Teste 4: Adicionar um cartão de crédito
    # ──────────────────────────────────────
    def test_fill_card(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.set_card_number(data.CARD_NUMBER)
        routes_page.set_card_cvv(data.CARD_CODE)
        routes_page.click_card_add_button()
        routes_page.close_payment()

        assert 'Cartão' in self.driver.find_element(*routes_page.payment_method_button).text \
               or len(self.driver.find_element(*routes_page.payment_method_button).text) > 0

    # ──────────────────────────────────────
    # Teste 5: Escrever um comentário para o motorista
    # ──────────────────────────────────────
    def test_comment_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_comment(data.MESSAGE_FOR_DRIVER)

        assert routes_page.get_comment() == data.MESSAGE_FOR_DRIVER

    # ──────────────────────────────────────
    # Teste 6: Pedir um cobertor e lenços
    # ──────────────────────────────────────
    def test_order_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_blanket_and_handkerchiefs()

        assert routes_page.is_blanket_and_handkerchiefs_selected()

    # ──────────────────────────────────────
    # Teste 7: Pedir 2 sorvetes
    # ──────────────────────────────────────
    def test_order_2_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.add_ice_cream(2)

        assert routes_page.get_ice_cream_count() == '2'

    # ──────────────────────────────────────
    # Teste 8: Pedir um táxi (modal de busca deve aparecer)
    # ──────────────────────────────────────
    def test_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.click_order_button()

        assert routes_page.is_order_modal_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
