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
        try:
            headers_dict = dict(headers)
        except Exception:
            headers_dict = headers
        logging.debug("REQUEST HEADERS:\n%s", json.dumps(headers_dict, indent=4, ensure_ascii=False))


    if payload:
        logging.debug("PAYLOAD REQUEST:\n%s", json.dumps(payload, indent=4, ensure_ascii=False))
  
    # Manejar respuestas sin contenido (como 204 No Content)
    try:
        if response.content and len(response.content) > 0:
            logging.debug("RESPONSE:\n%s", json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            logging.debug("RESPONSE: No content (empty body)")
    except (json.JSONDecodeError, ValueError):
        logging.debug("RESPONSE: %s (non-JSON content)", response.text if response.text else "No content")