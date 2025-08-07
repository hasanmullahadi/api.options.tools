import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from ..models.responses import (
    OptionsChain, OptionsFlow, SECFiling, 
    AnalysisResult, PortfolioOptimization
)
from ..utils.exceptions import (
    OptionsToolsError, AuthenticationError, 
    RateLimitError, ValidationError
)
import logging

logger = logging.getLogger(__name__)

class OptionsToolsClient:
    def __init__(
        self, 
        api_key: str,
        base_url: str = "https://api.options.tools",
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "options-tools-python/1.0.0"
            },
            timeout=httpx.Timeout(timeout)
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        await self.client.aclose()
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        url = f"/api/v1{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json
                )
                
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                elif response.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                elif response.status_code == 400:
                    raise ValidationError(response.json().get("detail", "Validation error"))
                elif response.status_code >= 500:
                    if attempt < self.max_retries - 1:
                        continue
                    raise OptionsToolsError(f"Server error: {response.status_code}")
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "error":
                    raise OptionsToolsError(data.get("error", {}).get("message", "Unknown error"))
                
                return data.get("data", data)
                
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    continue
                raise OptionsToolsError("Request timeout")
            except httpx.RequestError as e:
                if attempt < self.max_retries - 1:
                    continue
                raise OptionsToolsError(f"Request failed: {str(e)}")
    
    # Options Methods
    async def get_options_chain(
        self, 
        ticker: str,
        expiration: Optional[date] = None,
        strike: Optional[float] = None,
        option_type: Optional[str] = None
    ) -> OptionsChain:
        params = {"ticker": ticker.upper()}
        if expiration:
            params["expiration"] = expiration.isoformat()
        if strike:
            params["strike"] = strike
        if option_type:
            params["type"] = option_type
        
        data = await self._request("GET", f"/options/chain/{ticker}", params=params)
        return OptionsChain(**data)
    
    async def get_options_flow(
        self,
        ticker: str,
        timeframe: str = "1d",
        min_premium: Optional[float] = None,
        unusual_only: bool = False
    ) -> OptionsFlow:
        params = {
            "timeframe": timeframe,
            "unusual_only": unusual_only
        }
        if min_premium:
            params["min_premium"] = min_premium
        
        data = await self._request("GET", f"/options/flow/{ticker}", params=params)
        return OptionsFlow(**data)
    
    # SEC Methods
    async def get_sec_filings(
        self,
        ticker: str,
        filing_type: Optional[str] = None,
        limit: int = 10
    ) -> List[SECFiling]:
        params = {"limit": limit}
        if filing_type:
            params["filing_type"] = filing_type
        
        data = await self._request("GET", f"/sec/filings/{ticker}", params=params)
        return [SECFiling(**filing) for filing in data]
    
    # Analysis Methods
    async def get_entry_analysis(
        self,
        ticker: str,
        capital: Optional[float] = None,
        risk_tolerance: str = "moderate"
    ) -> AnalysisResult:
        params = {"risk_tolerance": risk_tolerance}
        if capital:
            params["capital"] = capital
        
        data = await self._request("GET", f"/analysis/entry/{ticker}", params=params)
        return AnalysisResult(**data)
    
    async def get_exit_analysis(
        self,
        ticker: str,
        entry_price: float,
        current_position: Dict[str, Any]
    ) -> AnalysisResult:
        json_data = {
            "entry_price": entry_price,
            "position": current_position
        }
        
        data = await self._request("POST", f"/analysis/exit/{ticker}", json=json_data)
        return AnalysisResult(**data)
    
    # Portfolio Methods
    async def optimize_portfolio(
        self,
        capital: float,
        tickers: List[str],
        strategy: str = "balanced",
        risk_level: str = "moderate"
    ) -> PortfolioOptimization:
        json_data = {
            "capital": capital,
            "tickers": tickers,
            "strategy": strategy,
            "risk_level": risk_level
        }
        
        data = await self._request("POST", "/portfolio/optimize", json=json_data)
        return PortfolioOptimization(**data)
    
    # Utility Methods
    async def health_check(self) -> Dict[str, Any]:
        response = await self.client.get("/health")
        return response.json()
    
    async def get_api_usage(self) -> Dict[str, Any]:
        data = await self._request("GET", "/account/usage")
        return data

# Synchronous wrapper for convenience
class OptionsTools:
    def __init__(self, api_key: str, **kwargs):
        self._client = OptionsToolsClient(api_key, **kwargs)
        self._loop = None
    
    def _run_async(self, coro):
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        
        if loop is None:
            return asyncio.run(coro)
        else:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
    
    def get_options_chain(self, *args, **kwargs):
        return self._run_async(self._client.get_options_chain(*args, **kwargs))
    
    def get_options_flow(self, *args, **kwargs):
        return self._run_async(self._client.get_options_flow(*args, **kwargs))
    
    def get_sec_filings(self, *args, **kwargs):
        return self._run_async(self._client.get_sec_filings(*args, **kwargs))
    
    def get_entry_analysis(self, *args, **kwargs):
        return self._run_async(self._client.get_entry_analysis(*args, **kwargs))
    
    def optimize_portfolio(self, *args, **kwargs):
        return self._run_async(self._client.optimize_portfolio(*args, **kwargs))