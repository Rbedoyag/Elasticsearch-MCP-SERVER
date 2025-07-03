import os
from dotenv import load_dotenv

from src.clients.common.client import SearchClient
from src.clients.exceptions import handle_search_exceptions

def create_search_client(engine_type: str) -> SearchClient:
    """
    Create a search client for the specified engine type.
    
    Args:
        engine_type: Type of search engine to use ("elasticsearch" or "opensearch")
        
    Returns:
        A search client instance
    """
    # Load .env if present
    load_dotenv()
    
    config = {}

    # Elastic Cloud override
    cloud_id = os.environ.get("ELASTIC_CLOUD_ID")
    api_key = os.environ.get("ELASTIC_API_KEY")
    
    if engine_type == "elasticsearch" and cloud_id and api_key:
        config["cloud_id"] = cloud_id
        config["api_key"] = api_key
        config["verify_certs"] = True  # Siempre recomendado en Elastic Cloud
    else:
        prefix = engine_type.upper()
        hosts_str = os.environ.get(f"{prefix}_HOSTS", "https://localhost:9200")
        hosts = [host.strip() for host in hosts_str.split(",")]
        username = os.environ.get(f"{prefix}_USERNAME")
        password = os.environ.get(f"{prefix}_PASSWORD")
        verify_certs = os.environ.get(f"{prefix}_VERIFY_CERTS", "false").lower() == "true"
        
        config = {
            "hosts": hosts,
            "username": username,
            "password": password,
            "verify_certs": verify_certs
        }
    
    return SearchClient(config, engine_type)

__all__ = [
    'create_search_client',
    'handle_search_exceptions',
    'SearchClient',
]
