import json
import time


def retrieve_phone_code(driver):
    """Retorna o código de confirmação do telefone.
    Usa JavaScript para interceptar respostas XHR/fetch no navegador.
    Deve ser chamado ANTES de clicar no botão Próximo.
    """
    # Injeta interceptador de XHR e fetch
    driver.execute_script("""
        window._phoneCode = null;
        var origOpen = XMLHttpRequest.prototype.open;
        var origSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.open = function() {
            this._url = arguments[1];
            origOpen.apply(this, arguments);
        };
        XMLHttpRequest.prototype.send = function() {
            var xhr = this;
            xhr.addEventListener('load', function() {
                try {
                    var data = JSON.parse(xhr.responseText);
                    if (data && data.code) {
                        window._phoneCode = data.code;
                    }
                } catch(e) {}
            });
            origSend.apply(this, arguments);
        };
        var origFetch = window.fetch;
        window.fetch = function() {
            return origFetch.apply(this, arguments).then(function(response) {
                response.clone().json().then(function(data) {
                    if (data && data.code) {
                        window._phoneCode = data.code;
                    }
                }).catch(function() {});
                return response;
            });
        };
    """)


def get_phone_code(driver):
    """Recupera o código SMS capturado pelo interceptador JavaScript."""
    for i in range(20):
        code = driver.execute_script("return window._phoneCode;")
        if code:
            return str(code)
        time.sleep(1)
    raise Exception(
        "Não foi possível obter o código de confirmação do telefone.\n"
        "Verifique se o pop-up de confirmação do telefone apareceu."
    )


def is_url_reachable(url):
    """Verifica se a URL do servidor Urban Routes é acessível."""
    import requests
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception:
        return False