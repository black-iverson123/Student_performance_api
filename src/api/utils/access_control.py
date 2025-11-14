from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

PERMISSIONS = {
    "sub_admin": {
        "courses": ['create', 'get_all', 'get_one', 'update', 'view'],
        "students": ['create', 'get_all', 'get_one', 'update'],
        "grades": ['upload', 'update','view'],
        "users": ['create', 'update', 'view'],
        "analytics": '*'
    },
    "teacher": {
        "courses": ['get_one', 'update', 'view'],
        "students": ['get_all', 'get_one'],
        "grades": ['upload','view'],
        "analytics": ['view']
    },
    "admin": {
        "courses": "*",
        "students": "*",
        "grades": "*",
        "users": "*",
        "analytics": "*"
    }
}

def permission_required(resource, action):
    """
    Decorator to check if the user's role has the required permission for a resource.
    :param resource: the resource to access, e.g., 'grades', 'students'
    :param action: the action to perform, e.g., 'create', 'view', 'update'
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if not role:
                return jsonify({"message": "Role not found in token"}), 403
            
            role_permissions = PERMISSIONS.get(role, {})
            allowed_actions = role_permissions.get(resource)
            
            # If permissions are '*' (all actions allowed)
            if allowed_actions == "*" or allowed_actions == ['*']:
                return func(*args, **kwargs)
            
            if allowed_actions is None or action not in allowed_actions:
                return jsonify({"message": f"Permission denied for {role} on {resource}:{action}"}), 403
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
