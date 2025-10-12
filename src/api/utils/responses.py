from flask import make_response, jsonify

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Invalid fields found"
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameters",
    "message": "Missing parameters"
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad Request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

UNAUTHORIZED_403 = {
    "http_code": 403,
    "code": "notAuthorised",
    "message": "You're not authorised to execute this."
}

SUCCESS_200 = {
    "http_code": 200,
    "code": "success",
    "message": ""
}

SUCCESS_201 = {
    "http_code": 201,
    "code": "success"
}

SUCCESS_202 = {
    "http_code": 202,
    "code": "success",
    "message":""
}

SERVER_ERROR_401 = {
    "http_code": 401,
    "code": "unauthorized"
}

DUPLICATE_ENTRY_409 = {
    "http_code": 409,
    "code": "conflict",
    "message": "user with this credentials already exists"
}

data =  {"message": "Students Performance Manager API",
                "creator": "black-iverson123",
                "profile": "https://github.com/black-iverson123"}


def response_with(response, value=None, message=None, error=None, headers={}, pagination=None):
    result = {}

    if value is not None:
        result.update(value)
    
    if message is not None:
        result.update({'message': message})
    elif response.get('message', None) is not None:
        result.update({'message': response['message']})
    
    result.update({'code': response['code']})

    if error is not None:
        result.update({'errors':error})
    
    if pagination is not None:
        result.update({'pagination': pagination})
    
    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'Flask Rest API'})

    return make_response(jsonify(result), response['http_code'], headers)