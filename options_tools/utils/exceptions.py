class OptionsToolsError(Exception):
    """Base exception for Options.tools API errors"""
    pass

class AuthenticationError(OptionsToolsError):
    """Raised when API key is invalid or missing"""
    pass

class RateLimitError(OptionsToolsError):
    """Raised when rate limit is exceeded"""
    pass

class ValidationError(OptionsToolsError):
    """Raised when request validation fails"""
    pass

class DataNotFoundError(OptionsToolsError):
    """Raised when requested data is not found"""
    pass

class ServerError(OptionsToolsError):
    """Raised when server returns 5xx error"""
    pass

class NetworkError(OptionsToolsError):
    """Raised when network request fails"""
    pass