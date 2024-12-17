import aiohttp
import asyncio
from typing import Dict, Optional, Any
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging

from app.core.config import get_settings
from app.services.proxy_manager import ProxyManager

logger = logging.getLogger(__name__)
settings = get_settings()

class Scraper:
    def __init__(self):
        self.ua = UserAgent()
        self.proxy_manager = ProxyManager()
        
    async def get_headers(self, custom_headers: Optional[Dict] = None) -> Dict:
        """Generate headers with random User-Agent"""
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers
        
    async def fetch(self, url: str, headers: Optional[Dict] = None, 
                   cookies: Optional[Dict] = None, proxy: Optional[str] = None,
                   timeout: int = 30) -> Dict[str, Any]:
        """Fetch URL with retry mechanism and proxy support"""
        try:
            async with aiohttp.ClientSession(cookies=cookies) as session:
                headers = await self.get_headers(headers)
                proxy = proxy or await self.proxy_manager.get_proxy()
                
                async with session.get(url, headers=headers, proxy=proxy, 
                                    timeout=timeout) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {
                            "success": True,
                            "status": response.status,
                            "content": content,
                            "headers": dict(response.headers),
                            "url": str(response.url)
                        }
                    else:
                        return {
                            "success": False,
                            "status": response.status,
                            "error": f"HTTP {response.status}",
                            "url": str(response.url)
                        }
                        
        except asyncio.TimeoutError:
            return {"success": False, "error": "Request timeout", "url": url}
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return {"success": False, "error": str(e), "url": url}
            
    async def parse(self, content: str, parser: str = "html.parser") -> BeautifulSoup:
        """Parse HTML content using BeautifulSoup"""
        return BeautifulSoup(content, parser)
        
    async def extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Any]:
        """Extract data from parsed HTML using CSS selectors"""
        result = {}
        for key, selector in selectors.items():
            elements = soup.select(selector)
            result[key] = [el.get_text(strip=True) for el in elements]
        return result
