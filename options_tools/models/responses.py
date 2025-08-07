from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class Option(BaseModel):
    strike: float
    expiration: date
    type: str  # call or put
    bid: Optional[float]
    ask: Optional[float]
    last: Optional[float]
    volume: Optional[int]
    open_interest: Optional[int]
    implied_volatility: Optional[float]
    delta: Optional[float]
    gamma: Optional[float]
    theta: Optional[float]
    vega: Optional[float]

class OptionsChain(BaseModel):
    ticker: str
    spot_price: float
    timestamp: datetime
    options: List[Option]

class FlowOrder(BaseModel):
    timestamp: datetime
    ticker: str
    strike: float
    expiration: date
    type: str
    size: int
    premium: float
    is_sweep: bool
    is_unusual: bool
    sentiment: str  # bullish, bearish, neutral

class OptionsFlow(BaseModel):
    ticker: str
    timeframe: str
    orders: List[FlowOrder]
    total_premium: float
    bullish_premium: float
    bearish_premium: float
    unusual_count: int

class SECFiling(BaseModel):
    ticker: str
    filing_type: str
    filing_date: date
    accession_number: str
    url: str
    parsed_data: Dict[str, Any]

class Signal(BaseModel):
    type: str  # buy, sell, hold
    strength: float  # 0-100
    reason: str
    confidence: float

class AnalysisResult(BaseModel):
    ticker: str
    timestamp: datetime
    signals: List[Signal]
    recommended_action: str
    risk_score: float
    expected_return: float
    stop_loss: Optional[float]
    take_profit: Optional[float]

class PortfolioRecommendation(BaseModel):
    ticker: str
    allocation: float
    strategy: str
    expected_return: float
    risk: float
    options_trades: List[Dict[str, Any]]

class PortfolioOptimization(BaseModel):
    total_capital: float
    recommendations: List[PortfolioRecommendation]
    expected_portfolio_return: float
    portfolio_risk: float
    sharpe_ratio: float