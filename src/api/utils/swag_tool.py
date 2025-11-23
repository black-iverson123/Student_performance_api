swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Student Performance Manager API",
        "description": "Documentation for APIs",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    }
}