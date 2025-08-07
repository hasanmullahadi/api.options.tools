"""
Options.tools - Professional options and market analysis API client

A comprehensive Python client for accessing real-time options data, SEC filings,
and proprietary trading analysis through the Options.tools API.
"""

__version__ = "1.0.0"
__author__ = "Hasan Mohammad"
__email__ = "contact@options.tools"

from .client.client import OptionsTools, OptionsToolsClient
from .utils.exceptions import (
    OptionsToolsError,
    AuthenticationError,
    RateLimitError,
    ValidationError
)

__all__ = [
    "OptionsTools",
    "OptionsToolsClient",
    "OptionsToolsError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
]

# Convenience function for quick setup
def create_client(api_key: str, **kwargs) -> OptionsTools:
    """
    Create an Options.tools client instance.
    
    Args:
        api_key: Your Options.tools API key
        **kwargs: Additional configuration options
        
    Returns:
        OptionsTools client instance
        
    Example:
        >>> import options_tools
        >>> client = options_tools.create_client("your_api_key")
        >>> chain = client.get_options_chain("AAPL")
    """
    return OptionsTools(api_key, **kwargs)