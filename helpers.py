# helpers.py — Funções auxiliares para os testes do Urban Routes

import json
import time
from selenium.common.exceptions import WebDriverException


def retrieve_phone_code(driver):
    """Retorna o código de confirmação do telefone.
    Intercepta requisições feitas ao servidor para obter o código SMS.
    O pop-up de confirmação do telefone deve estar aberto antes de chamar este método.
    """
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")]
            for log in reversed(logs):
                log_data = json.loads(log)
                body = log_data.get("message", {}).get("params", {}).get("response", {}).get("body")
                if body:
                    json_body = json.loads(body)
                    if "code" in json_body:
                        code = json_body["code"]
                        return code
        except WebDriverException:
            time.sleep(1)
            continue
    raise Exception(
        "Não foi possível obter o código de confirmação do telefone.\n"
        "Verifique se o pop-up de confirmação do telefone apareceu e se o código foi enviado."
    )


def is_url_reachable(url):
    """Verifica se a URL do servidor Urban Routes é acessível."""
    import requests
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception:
        return False
