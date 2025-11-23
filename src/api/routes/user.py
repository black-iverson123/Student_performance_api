"""
Module for user routes
_ Create, Read, Update and Delete Methods
"""

from flask import Blueprint, request, g
from src.api.utils.database import db
from src.api.models.user import User
from src.api.schema.user_schema import UserSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.access_control import permission_required
from src.api.utils.helper import get_school_context
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token, create_refresh_token
from flasgger import swag_from
import logging

#setting logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Create abd register blueprint for user_routes
user_routes = Blueprint("user_routes", __name__)  

# context handler
@user_routes.before_request
@jwt_required()
def load_jwt_context():
    """
    Automatically loads school_id and user_email from the JWT into Flask's global context (g)
    for every request that includes a valid JWT. If no JWT is provided, g remains empty.
    """
    try:
        claims = get_jwt()
        identity = get_jwt_identity()

        if claims:
            g.school_id = claims.get('school_id')
        else:
            g.school_id = None

        g.user_email = identity
    except Exception as e:
        # Handles routes where JWT isn't required or is missing
        g.school_id = None
        g.user_email = None
        logging.debug(f"Alert: JWT context not set: {e}")

#Routes
@user_routes.post('/')
@jwt_required()
@permission_required('users', 'create')
@swag_from('../docs/user/create_user.yml')
def create_user():
    """Create a new user"""
    data = get_school_context(request.get_json())
    data["school_id"] = g.school_id

    user_schema = UserSchema()
    user = user_schema.load(data)

    try:
        result = user_schema.dump(user.create())
        return response_with(
                            resp.SUCCESS_201,
                            value={"user": result},
                            message=f"You've successfully added {user.firstname}"
                        )
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.BAD_REQUEST_400, )


@user_routes.get('/')
@jwt_required()
@permission_required('users', 'view')
@swag_from('../docs/user/get_users.yml')
def get_users():
    """Retrieve all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    query = User.query.filter_by(school_id=g.school_id)
    users = query.offset((page - 1) * per_page).limit(per_page).all()
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    return response_with(resp.SUCCESS_200, value={"users": data},
                            pagination={
                                "page": page,
                                "per_page": per_page,
                                "total": query.count()})

@user_routes.get('/<int:user_id>')
@jwt_required()
@permission_required('users', 'view')
@swag_from('../docs/user/get_user.yml')
def get_user(user_id):
    """Retrieve a single user"""
    user = User.query.filter_by(school_id=g.school_id, id=user_id).first()
    if not user:
        return response_with(resp.VALIDATION_ERROR_422, message="User not found")
    try: 
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return response_with(resp.SUCCESS_200, value={"user": data})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.INTERNAL_SERVER_ERROR_500)

@user_routes.patch('/<int:user_id>')
@jwt_required()
@permission_required('users', 'update')
@swag_from('../docs/user/update_user.yml')
def update_user(user_id):
    """Update a specific user"""
    data = request.get_json()
    user = User.query.filter_by(school_id=g.school_id, id=user_id).first()

    if not user:
        return response_with(resp.VALIDATION_ERROR_422, message="User not found")

    try:
        user_schema = UserSchema(partial=True)
        user = user_schema.load(data, instance=user)
        db.session.commit()

        result = user_schema.dump(user)
        return response_with(resp.SUCCESS_200, value={"user": result}, message="User updated successfully")

    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        db.session.rollback()
        return response_with(resp.INTERNAL_SERVER_ERROR_500, message="Error updating user")

@user_routes.delete('/<int:user_id>')
@jwt_required()
@permission_required('users', 'delete')
@swag_from('../docs/user/delete_user.yml')
def delete_user(user_id):
    """Remove a user from database"""
    user = User.query.filter_by(school_id=g.school_id, id=user_id).first()
    if not user:
        return response_with(resp.VALIDATION_ERROR_422, message="User not found")

    try:
        db.session.delete(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, message="User deleted successfully")
    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        db.session.rollback()
        return response_with(resp.INTERNAL_SERVER_ERROR_500, message="Error deleting user")