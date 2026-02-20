import json
import logging
import os
import time
from typing import Any, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv
from langchain_community.tools import tool
import requests

load_dotenv()

@tool
def api_query_base_on_itemId(item_id: str) -> str:
    """
    This a product query function that returns a string product information via api call based on the itemId.

    Input: itemId of the item, only number nothing else (e.g., "58170")
    
    Output: The name and category of the item as a string (e.g., "The name of item 58170 is: ... and the category is: ...")
    
    """
    config = APIConfig(api_key=os.getenv("PIA_GATEWAY_TOKEN"))
    fetcher = APIFetcher(config)
    
    try:
        data = fetcher.fetch_item(item_id)
        data_category = data.get("category", "N/A")
        data_name = data.get("name", "N/A")
        print(f"API query result for itemId {item_id} - Name: {data_name}, Category: {data_category}") # for monitoring the API query result
        return f"The name of item {item_id} is: {data_name} and the category is: {data_category}"
    
    except Exception as e:
        return f"Error: {str(e)}"


@dataclass
class APIConfig:
    base_url: str = "https://gw-stage.int.csi-api.axis.com/int/pia_ext_stage/3.31.0"
    timeout: int = 30
    retry_count: int = 3
    retry_delay: int = 2
    api_key: Optional[str] = None  # API密钥（从环境变量读取）
    auth_header: str = "Authorization"  # 认证头名称
    auth_prefix: str = "Bearer"  # 认证前缀 (Bearer/ApiKey等)


class APIFetcher:
    
    def __init__(self, config: Optional[APIConfig] = None):

        self.config = config or APIConfig() # initialize with default config if not provided
        self.session = requests.Session() # init session for connection pooling
        
        # set default headers
        self.session.headers["accept"] = "application/json" # tell the server we want JSON response

        # set authentication settings in header
        auth_value = f"{self.config.auth_prefix} {self.config.api_key}".strip() # Bearer <token>
        self.session.headers[self.config.auth_header] = auth_value # Authorization : Bearer <token>
    
    
    
    def fetch_item(self, item_id: str) -> Dict[str, Any]:

        url = f"{self.config.base_url}/items/{item_id}"
        return self._fetch_with_retry(url)
    
    def _fetch_with_retry(self, url: str) -> Dict[str, Any]:
        """带重试的数据获取"""
        
        for attempt in range(1, self.config.retry_count + 1):
            
            try:
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                
                data = response.json()
                return data
            
            except requests.exceptions.RequestException as e:
                
                if attempt == self.config.retry_count:
                    raise
                time.sleep(self.config.retry_delay)
        
        raise RuntimeError("Unexpected retry loop exit")
    
    def close(self):
        self.session.close()


"""
def main():

    import os
    
    config = APIConfig(
        api_key=os.getenv("PIA_GATEWAY_TOKEN")
    )

    fetcher = APIFetcher(config)
    
    try:
        item_id = "58170"
        data = fetcher.fetch_item(item_id)
        data_category = data.get("category", "N/A")
        data_name = data.get("name", "N/A")
    
        print(f"Categories of item {item_id} is: {data_category}")
        print(f"Name of item {item_id} is: {data_name}")
        
    except Exception as e:
        print(f"\nError: {e}")
        
    finally:
        fetcher.close()


if __name__ == "__main__":
    main()
"""