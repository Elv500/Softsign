import logging
import json

def log_request_response(url, response, headers=None, payload=None):
    """
    INFO:  IP Address o dominio
    DEBUG: Request URL + Headers
    DEBUG: Payloads (datos enviados en el request)
    INFO:  Status Code
    DEBUG: Response (body o json de respuesta) 
    """
    logging.info("IP ADDRESS OR DOMAIN: %s", url.split("/")[2])
    logging.debug("REQUEST URL: %s", url)
    logging.info("STATUS CODE: %s", response.status_code)
    
    if headers:
        logging.debug("REQUEST HEADERS:\n%s", json.dumps(headers, indent=4, ensure_ascii=False))

    if payload:
        logging.debug("PAYLOAD REQUEST:\n%s", json.dumps(payload, indent=4, ensure_ascii=False))
  
    # Manejo seguro de respuestas - evitar errores con respuestas 522, 404, etc.
    try:
        if response.status_code == 200 and response.headers.get('content-type', '').startswith('application/'):
            logging.debug("RESPONSE:\n%s", json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            # Para códigos de error o respuestas no-JSON, solo mostrar el texto
            logging.debug("RESPONSE TEXT:\n%s", response.text[:500] + "..." if len(response.text) > 500 else response.text)
    except Exception as e:
        logging.debug("RESPONSE (error parsing): %s - Text: %s", str(e), response.text[:200])