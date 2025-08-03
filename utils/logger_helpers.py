import logging
import json

def log_request_response(url, headers, response, payload=None):
    """
    INFO:  IP Address o dominio
    DEBUG: Request URL + Headers
    DEBUG: Payloads (datos enviados en el request)
    INFO:  Status Code
    DEBUG: Response (body o json de respuesta) 
    """
    logging.info("IP ADDRESS OR DOMAIN: %s", url.split("/")[2])
    logging.debug("REQUEST URL: %s", url)
    logging.debug("REQUEST HEADERS: %s", json.dumps(headers, indent=4, ensure_ascii=False))
    if payload is not None:
        logging.debug("PAYLOAD REQUEST: %s", json.dumps(payload, indent=4, ensure_ascii=False))
    logging.info("STATUS CODE: %s", response.status_code)
    logging.debug("RESPONSE: %s", json.dumps(response.json(), indent=4, ensure_ascii=False))