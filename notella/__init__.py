"""Notella: weave knowledge into understanding."""
from .core import Notella, ValidationError
from .client import Client

__version__ = '0.1.0'
__all__ = ['Notella', 'ValidationError', 'Client']
