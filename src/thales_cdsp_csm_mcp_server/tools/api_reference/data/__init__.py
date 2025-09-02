"""
Static Data Module

This module contains static data like response formats and best practices.
"""

from .response_formats import get_response_formats
from .best_practices import get_best_practices

__all__ = [
    'get_response_formats',
    'get_best_practices'
] 