import requests
import time
import logging

logger = logging.getLogger(__name__)

class SyliusRequest:
    # Timeout más alto para evitar errores 522
    DEFAULT_TIMEOUT = (10, 30)  # (connect timeout, read timeout)
    MAX_RETRIES = 2
    
    @staticmethod
    def _make_request(method, url, headers=None, payload=None, **kwargs):
        """
        Método privado para hacer peticiones con retry automático y timeout
        """
        headers = headers or {}
        
        for attempt in range(1, SyliusRequest.MAX_RETRIES + 1):
            try:
                logger.debug(f"Intento {attempt}/{SyliusRequest.MAX_RETRIES} para {method} {url}")
                
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, timeout=SyliusRequest.DEFAULT_TIMEOUT)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=headers, json=payload, timeout=SyliusRequest.DEFAULT_TIMEOUT)
                elif method.upper() == 'PUT':
                    response = requests.put(url, headers=headers, json=payload, timeout=SyliusRequest.DEFAULT_TIMEOUT)
                elif method.upper() == 'DELETE':
                    response = requests.delete(url, headers=headers, json=payload, timeout=SyliusRequest.DEFAULT_TIMEOUT)
                
                # Si obtenemos 522 (timeout del servidor), retry después de delay
                if response.status_code == 522 and attempt < SyliusRequest.MAX_RETRIES:
                    logger.warning(f"Recibido 522 en intento {attempt}. Esperando antes de retry...")
                    time.sleep(2)  # Esperar 2 segundos antes del retry
                    continue
                    
                return response
                
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                logger.warning(f"Error de conexión en intento {attempt}: {e}")
                if attempt < SyliusRequest.MAX_RETRIES:
                    time.sleep(1)  # Esperar 1 segundo antes del retry
                    continue
                raise
        
        return response

    @staticmethod
    def get(url, headers):
        return SyliusRequest._make_request('GET', url, headers)

    @staticmethod
    def post(url, headers=None, payload=None):
        if headers is None:
            headers = {}
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        return SyliusRequest._make_request('POST', url, headers, payload)

    @staticmethod
    def put(url, headers, payload=None):
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        return SyliusRequest._make_request('PUT', url, headers, payload)

    @staticmethod
    def delete(url, headers, payload=None):
        headers = headers.copy()
        headers.update({'Content-Type': 'application/json'})
        return SyliusRequest._make_request('DELETE', url, headers, payload)