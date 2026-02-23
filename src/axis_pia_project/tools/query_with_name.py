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
def api_query_base_on_name(item_name: str) -> str:
    """
    This a query function that returns itemIds via api call based on the item name.

    Input:  name of the item (e.g., "AXIS T8127","AXIS 210A Surveillance Kit").
    
    Output: The itemIds of the item as a string (e.g., "The itemId of AXIS T8127 is: 58170")
    
    """

    config = APIConfig(api_key=os.getenv("PIA_GATEWAY_TOKEN"))
    fetcher = itemIdFetcher(config)
    
    try:
        # Call the fetcher to get itemId based on the item name, which will try different types (Product, ProductVariant, SalesUnit)
        result = fetcher.fetch_item(item_name)
        
        if not result:
            return "Error: No itemId found for this product name"
      
        first_id = None

        # get the first itemId from the result 
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and 'id' in result[0]:
                first_id = result[0]['id']
   
        if first_id:
            print(f"\nThe itemId for '{item_name}' is: {first_id}")
            return str(first_id) 
        else:
            return "Error: Could not extract itemId from result"
    

    except Exception as e:
        return f"Error: {str(e)}"
    
    finally:
        fetcher.close()


@dataclass
class APIConfig:
    base_url: str = "https://gw-stage.int.csi-api.axis.com/int/pia_ext_stage/3.31.0"
    timeout: int = 30
    retry_count: int = 3
    retry_delay: int = 2
    api_key: Optional[str] = None  
    auth_header: str = "Authorization"  
    auth_prefix: str = "Bearer"  


class itemIdFetcher:
    
    def __init__(self, config: Optional[APIConfig] = None):

        self.config = config or APIConfig() # initialize with default config if not provided
        self.session = requests.Session() # init session for connection pooling

        # set default headers
        self.session.headers["accept"] = "application/json"

        # set authentication settings in header
        auth_value = f"{self.config.auth_prefix} {self.config.api_key}".strip() # Bearer <token>
        self.session.headers[self.config.auth_header] = auth_value # Authorization : Bearer <token>
    
    
    
    def fetch_item(self, item_name: str) -> Dict[str, Any]:

        # typeList = ["Line", "Series", "Model", "Product", "ProductVariant", "SalesUnit"] # iterate through different types to find the itemId

        typeList = ["Product", "ProductVariant", "SalesUnit"] 
        
        for type_name in typeList:
            print(f"\nQuerying type: {type_name}")

            api_call_parameters = {
                "type": type_name,
                "vendorType": "Axis",
                "q": item_name,
                "supportedRegExp": True, 
                "pageLimit": 10,
                "pageNum": 1,
                "fields": "id,none"
            }    
            
            url = f"{self.config.base_url}/items"
            
            try:
                # 调用 API 并收集数据
                data = self._fetch_with_retry(url, api_call_parameters)

                if data: 
                    return data  
                
            except Exception as e:
                print(f"  → Error querying {type_name}: {e}")
                continue
        

        print(f"  ✗ No results found in any type.")
        return None
    



    
    def _fetch_with_retry(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """带重试的数据获取"""
        
        for attempt in range(1, self.config.retry_count + 1):
            
            try:
                response = self.session.get(url, params=params, timeout=self.config.timeout)
                
                # when 404, check if the response message contains "does not contain any items", which means there is no item for this type, then return empty result instead of raising exception
                if response.status_code == 404:
                    try:
                        error_data = response.json()
                        if "does not contain any items" in error_data.get("message", ""):
                            print(f"  → No items found for this type")
                            return {} # there is no item for this type, and it can try other types
                    except:
                        pass
                
                response.raise_for_status() # raise exception for other 4xx/5xx errors


                data = response.json()

                
                if isinstance(data, list):
                    print(f"  → Found {len(data)} item(s)")

                print(f"  → The result is: {data}")

                return data  # 成功时返回数据
            
            except requests.exceptions.RequestException as e:
                if attempt < self.config.retry_count:
                    print(f"  → Attempt {attempt} failed, retrying...")
                    time.sleep(self.config.retry_delay)
                else:
                    # 最后一次尝试失败
                    print(f"  → Error: {e}")
                    raise
        
        raise RuntimeError("Unexpected retry loop exit")
    
    def close(self):
        self.session.close()


"""
def main():
    
    item_name = "M5000"
    
    print(f"{'='*60}")
    print(f"Testing query for: {item_name}")
    print('='*60)
    result = api_query_base_on_name.invoke({"item_name": item_name})
    print(f"\n{'='*60}")
    print(f"The first itemId of '{item_name}' is: {result}")
    print('='*60)


if __name__ == "__main__":
    main()
"""