"""
responses.py

Standardized API response definitions and helper function for Students Performance Manager API.

This module provides:
- Common HTTP response templates with clear messages and status codes.
- A helper function `response_with` to return JSON responses consistently.
- Useful for API consumers to handle success, validation, authorization, and server errors.

Author: black-iverson123
Profile: https://github.com/black-iverson123
"""

from flask import make_response, jsonify

# ---------------------------
# Client Error Responses (4xx)
# ---------------------------
INVALID_FIELD_NAME_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "One or more fields are invalid"
}

VALIDATION_ERROR_422 = {
    "http_code": 422,
    "code": "validationError",
    "message": "Invalid input or missing required fields"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameters",
    "message": "Required parameters are missing"
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

UNAUTHORIZED_401 = {
    "http_code": 401,
    "code": "unauthorized",
    "message": "Authentication required or token invalid/expired"
}

FORBIDDEN_403 = {
    "http_code": 403,
    "code": "forbidden",
    "message": "You do not have permission to perform this action"
}

NOT_FOUND_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

CONFLICT_409 = {
    "http_code": 409,
    "code": "conflict",
    "message": "Resource conflict: duplicate entry"
}

# ---------------------------
# Server Error Responses (5xx)
# ---------------------------
INTERNAL_SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Internal server error occurred"
}

# ---------------------------
# Success Responses (2xx)
# ---------------------------
SUCCESS_200 = {
    "http_code": 200,
    "code": "success",
    "message": "Request completed successfully"
}

SUCCESS_201 = {
    "http_code": 201,
    "code": "success",
    "message": "Resource created successfully"
}

SUCCESS_202 = {
    "http_code": 202,
    "code": "success",
    "message": "Request accepted for processing"
}

# ---------------------------
# Meta information
# ---------------------------
data = {
    "message": "Students Performance Manager API",
    "creator": "black-iverson123",
    "profile": "https://github.com/black-iverson123"
}

# ---------------------------
# Response helper
# ---------------------------
def response_with(response, value=None, message=None, error=None, headers=None, pagination=None):
    """
    Returns a standardized JSON response for API endpoints.

    Args:
        response (dict): Predefined response template from this module.
        value (dict, optional): Data to include in the response.
        message (str, optional): Custom message to override default.
        error (dict or list, optional): Error details.
        headers (dict, optional): Additional HTTP headers.
        pagination (dict, optional): Pagination metadata if applicable.

    Returns:
        Response: Flask response object with JSON body and HTTP status code.
    """
    if headers is None:
        headers = {}

    result = {}

    if value is not None:
        result.update(value)

    if message is not None:
        result['message'] = message
    else:
        result['message'] = response.get('message', '')

    result['code'] = response['code']

    if error is not None:
        result['errors'] = error

    if pagination is not None:
        result['pagination'] = pagination

    # Default headers
    headers.update({
        'Access-Control-Allow-Origin': '*',
        'Server': 'Flask Rest API'
    })

    return make_response(jsonify(result), response['http_code'], headers)
