# Options.tools Python Client

Professional options and market analysis API client for Python.

## Installation

```bash
pip install options-tools
```

## Quick Start

```python
import options_tools

# Create client
client = options_tools.create_client("your_api_key")

# Get options chain
chain = client.get_options_chain("AAPL")

# Get unusual options flow
flow = client.get_options_flow("NVDA", timeframe="1d")

# Get SEC filings
filings = client.get_sec_filings("TSLA", filing_type="10-K")

# Get entry analysis
analysis = client.get_entry_analysis("SPY", capital=10000)
```

## Async Usage

```python
import asyncio
from options_tools import OptionsToolsClient

async def main():
    async with OptionsToolsClient("your_api_key") as client:
        chain = await client.get_options_chain("AAPL")
        print(chain)

asyncio.run(main())
```

## Features

- 📊 Real-time options chains with Greeks
- 🔍 Unusual options activity detection
- 📑 SEC filing analysis
- 🎯 Proprietary entry/exit signals
- 💼 Portfolio optimization
- 🤖 MCP integration for AI models

## API Key

Get your API key at [https://options.tools](https://options.tools)

## Documentation

Full documentation available at [https://docs.options.tools](https://docs.options.tools)

## License

MIT License - See LICENSE file for details