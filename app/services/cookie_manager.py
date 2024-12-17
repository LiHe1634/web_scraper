from typing import Dict, Optional
import json
import aiohttp
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CookieManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.cookie_key_prefix = "cookies:"
        self.expiry_key_prefix = "cookie_expiry:"
        
    async def get_cookies(self, domain: str) -> Optional[Dict]:
        """获取指定域名的Cookie"""
        try:
            cookies = await self.redis.get(f"{self.cookie_key_prefix}{domain}")
            if cookies:
                return json.loads(cookies)
            return None
        except Exception as e:
            logger.error(f"Error getting cookies for {domain}: {str(e)}")
            return None
            
    async def save_cookies(self, domain: str, cookies: Dict, 
                          expiry: Optional[timedelta] = None):
        """保存Cookie信息"""
        try:
            await self.redis.set(
                f"{self.cookie_key_prefix}{domain}",
                json.dumps(cookies)
            )
            
            if expiry:
                expiry_time = datetime.utcnow() + expiry
                await self.redis.set(
                    f"{self.expiry_key_prefix}{domain}",
                    expiry_time.timestamp()
                )
        except Exception as e:
            logger.error(f"Error saving cookies for {domain}: {str(e)}")
            
    async def is_expired(self, domain: str) -> bool:
        """检查Cookie是否过期"""
        try:
            expiry = await self.redis.get(f"{self.expiry_key_prefix}{domain}")
            if not expiry:
                return True
                
            expiry_time = datetime.fromtimestamp(float(expiry))
            return datetime.utcnow() > expiry_time
        except Exception as e:
            logger.error(f"Error checking cookie expiry for {domain}: {str(e)}")
            return True
            
    async def refresh_cookies(self, domain: str, 
                            login_url: str,
                            credentials: Dict) -> bool:
        """刷新Cookie"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(login_url, json=credentials) as response:
                    if response.status == 200:
                        cookies = response.cookies
                        await self.save_cookies(
                            domain,
                            {k: v.value for k, v in cookies.items()},
                            expiry=timedelta(hours=24)
                        )
                        return True
            return False
        except Exception as e:
            logger.error(f"Error refreshing cookies for {domain}: {str(e)}")
            return False
            
    async def delete_cookies(self, domain: str):
        """删除Cookie"""
        try:
            await self.redis.delete(f"{self.cookie_key_prefix}{domain}")
            await self.redis.delete(f"{self.expiry_key_prefix}{domain}")
        except Exception as e:
            logger.error(f"Error deleting cookies for {domain}: {str(e)}")
            
    async def get_all_domains(self) -> list:
        """获取所有保存的Cookie域名"""
        try:
            keys = await self.redis.keys(f"{self.cookie_key_prefix}*")
            return [k.replace(self.cookie_key_prefix, "") for k in keys]
        except Exception as e:
            logger.error(f"Error getting cookie domains: {str(e)}")
            return []
