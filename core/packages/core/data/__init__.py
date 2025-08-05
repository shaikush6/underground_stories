"""
Underground Stories Data Management Package
==========================================

Hybrid JSON/Supabase data management with migration capability.
"""

from .data_manager import DataManager, get_data_manager

__all__ = ['DataManager', 'get_data_manager']