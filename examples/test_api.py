#!/usr/bin/env python3
"""
Test script for Options.tools API
Tests the workflow with GOOG (Google/Alphabet)
"""

import asyncio
import sys
import os
from datetime import date, datetime

# Add the public library to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'public'))

# Import our client library
from options_tools.client.client import OptionsToolsClient

async def test_api():
    """Test the API with GOOG"""
    
    # Create client with test API key
    client = OptionsToolsClient(
        api_key="test_api_key",
        base_url="http://localhost:8000"
    )
    
    print("="*60)
    print("OPTIONS.TOOLS API TEST - GOOG")
    print("="*60)
    
    try:
        # Test 1: Health Check
        print("\n1. Testing Health Check...")
        health = await client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Redis: {health.get('redis', 'N/A')}")
        
        # Test 2: Get Options Chain for GOOG
        print("\n2. Getting Options Chain for GOOG...")
        try:
            chain = await client.get_options_chain("GOOG")
            print(f"   Ticker: {chain.ticker}")
            print(f"   Spot Price: ${chain.spot_price}")
            print(f"   Options Count: {len(chain.options)}")
            
            if chain.options:
                first_option = chain.options[0]
                print(f"   Sample Option:")
                print(f"     - Strike: ${first_option.strike}")
                print(f"     - Type: {first_option.type}")
                print(f"     - Bid/Ask: ${first_option.bid}/{first_option.ask}")
                print(f"     - Delta: {first_option.delta}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 3: Get Options Flow for GOOG
        print("\n3. Getting Options Flow for GOOG...")
        try:
            flow = await client.get_options_flow("GOOG", timeframe="1d")
            print(f"   Total Premium: ${flow.total_premium:,.2f}")
            print(f"   Bullish Premium: ${flow.bullish_premium:,.2f}")
            print(f"   Bearish Premium: ${flow.bearish_premium:,.2f}")
            print(f"   Unusual Orders: {flow.unusual_count}")
            
            if flow.orders:
                print(f"   Recent Order:")
                order = flow.orders[0]
                print(f"     - Strike: ${order.strike}")
                print(f"     - Size: {order.size} contracts")
                print(f"     - Premium: ${order.premium:,.2f}")
                print(f"     - Sentiment: {order.sentiment}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 4: Get SEC Filings for GOOG
        print("\n4. Getting SEC Filings for GOOG...")
        try:
            filings = await client.get_sec_filings("GOOG", limit=5)
            print(f"   Found {len(filings)} filings")
            
            for filing in filings[:3]:
                print(f"   - {filing.filing_type} on {filing.filing_date}")
                if hasattr(filing, 'parsed_data') and filing.parsed_data:
                    if filing.filing_type == '8-K' and 'events' in filing.parsed_data:
                        print(f"     Events: {', '.join(filing.parsed_data['events'])}")
                    elif filing.filing_type in ['10-K', '10-Q'] and 'financial_highlights' in filing.parsed_data:
                        highlights = filing.parsed_data['financial_highlights']
                        print(f"     Revenue: ${highlights.get('revenue', 0):,.0f}")
                        print(f"     Net Income: ${highlights.get('net_income', 0):,.0f}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 5: Get Entry Analysis for GOOG
        print("\n5. Getting Entry Analysis for GOOG...")
        try:
            analysis = await client.get_entry_analysis("GOOG", capital=10000)
            print(f"   Recommended Action: {analysis.recommended_action}")
            print(f"   Risk Score: {analysis.risk_score}/10")
            print(f"   Expected Return: {analysis.expected_return*100:.1f}%")
            
            if analysis.signals:
                signal = analysis.signals[0]
                print(f"   Signal: {signal.type.upper()}")
                print(f"   Strength: {signal.strength}/100")
                print(f"   Reason: {signal.reason}")
            
            if hasattr(analysis, 'stop_loss') and analysis.stop_loss:
                print(f"   Stop Loss: ${analysis.stop_loss}")
            if hasattr(analysis, 'take_profit') and analysis.take_profit:
                print(f"   Take Profit: ${analysis.take_profit}")
        except Exception as e:
            print(f"   Error: {e}")
        
        # Test 6: Portfolio Optimization
        print("\n6. Testing Portfolio Optimization...")
        try:
            portfolio = await client.optimize_portfolio(
                capital=100000,
                tickers=["GOOG", "AAPL", "MSFT"],
                strategy="balanced"
            )
            print(f"   Total Capital: ${portfolio.total_capital:,.2f}")
            print(f"   Expected Return: {portfolio.expected_portfolio_return*100:.1f}%")
            print(f"   Portfolio Risk: {portfolio.portfolio_risk*100:.1f}%")
            print(f"   Sharpe Ratio: {portfolio.sharpe_ratio:.2f}")
            
            print(f"   Allocations:")
            for rec in portfolio.recommendations:
                print(f"     - {rec.ticker}: ${rec.allocation:,.2f}")
                if rec.options_trades:
                    trade = rec.options_trades[0]
                    print(f"       Strategy: {trade['type']}")
                    print(f"       Contracts: {trade['contracts']}")
        except Exception as e:
            print(f"   Error: {e}")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        await client.close()
        print("\n" + "="*60)
        print("TEST COMPLETE")
        print("="*60)

async def test_direct_sec():
    """Test SEC API directly"""
    print("\n" + "="*60)
    print("DIRECT SEC EDGAR API TEST")
    print("="*60)
    
    import httpx
    
    headers = {
        "User-Agent": "OptionsTools Test test@options.tools"
    }
    
    async with httpx.AsyncClient() as client:
        # Get company tickers
        print("\nFetching company data from SEC...")
        response = await client.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=headers
        )
        
        if response.status_code == 200:
            companies = response.json()
            
            # Find Google
            goog_info = None
            for company in companies.values():
                if company.get("ticker") == "GOOG":
                    goog_info = company
                    break
            
            if goog_info:
                print(f"Found GOOG:")
                print(f"  Company: {goog_info.get('title')}")
                print(f"  CIK: {goog_info.get('cik_str')}")
                
                # Get recent filings
                cik = str(goog_info.get('cik_str')).zfill(10)
                print(f"\nFetching recent filings for CIK {cik}...")
                
                filing_response = await client.get(
                    f"https://data.sec.gov/submissions/CIK{cik}.json",
                    headers=headers
                )
                
                if filing_response.status_code == 200:
                    data = filing_response.json()
                    recent = data.get("filings", {}).get("recent", {})
                    
                    print(f"Recent filings:")
                    forms = recent.get("form", [])[:5]
                    dates = recent.get("filingDate", [])[:5]
                    
                    for form, date in zip(forms, dates):
                        print(f"  - {form} filed on {date}")
                else:
                    print(f"Failed to fetch filings: {filing_response.status_code}")
            else:
                print("GOOG not found in SEC data")
        else:
            print(f"Failed to fetch company data: {response.status_code}")

if __name__ == "__main__":
    print("\n🚀 Starting Options.tools API Tests\n")
    
    # Test the main API
    asyncio.run(test_api())
    
    # Test SEC directly
    asyncio.run(test_direct_sec())