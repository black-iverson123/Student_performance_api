"""
School Context Utility Module
=============================

This module provides helper functions to enrich incoming request data with 
contextual information from the currently authenticated user's JWT token. 
It is primarily used to attach school-related identifiers and the creator's 
email to request payloads.

Functions:
    get_school_context(data: Dict, creator=True) -> Dict
        Adds the logged-in user's school_id, admin_id, and email to the provided data.
"""

from flask_jwt_extended import get_jwt, get_jwt_identity
from typing import Dict

def get_school_context(data: Dict, creator=True) -> Dict:
    """
    Adds the current logged-in user's email and school id to the given data dictionary.
    if creator is to be signed as last modifier
    Args:
        data (dict): The incoming JSON data from the request module.

    Returns:
        dict: The updated data that includes the email.
    """
    email = get_jwt_identity()
    claims = get_jwt()
    if creator: 
        data['school_id'] = claims.get('school_id')
        data['created_by'] = email
        data['admin_id'] = claims.get('admin_id')
    return data
