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
    return data
