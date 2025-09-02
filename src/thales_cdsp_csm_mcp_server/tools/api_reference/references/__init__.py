"""
API Reference Data Module

This module contains all the reference data for different API endpoints.
"""

from .auth_reference import get_auth_reference
from .secrets_reference import get_create_secret_reference, get_get_secret_reference
from .workflow_reference import get_generic_workflow_reference
from .list_references import get_list_items_reference, get_list_roles_reference, get_list_targets_reference
from .other_references import get_delete_item_reference, get_codebase_scan_reference, get_secret_migration_reference

__all__ = [
    'get_auth_reference',
    'get_create_secret_reference', 
    'get_get_secret_reference',
    'get_generic_workflow_reference',
    'get_list_items_reference',
    'get_list_roles_reference',
    'get_list_targets_reference',
    'get_delete_item_reference',
    'get_codebase_scan_reference',
    'get_secret_migration_reference'
] 