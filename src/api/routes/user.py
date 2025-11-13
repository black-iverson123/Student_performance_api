from flask import Blueprint, request, g
from src.api.utils.database import db
from src.api.models.user import User
from src.api.schema.user_schema import UserSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.helper import get_school_context
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token, create_refresh_token
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

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
def create_user():
    data = get_school_context(request.get_json())
    print(data)
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
        return response_with(resp.INVALID_INPUT_422, )

@user_routes.post('/login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(
            identity=user.email,  # string identity
            additional_claims={"school_id": user.school_id, "admin_id": user.id}
        )
        refresh_token = create_refresh_token(
            identity=user.email,
            additional_claims={"school_id": user.school_id, "admin_id": user.id}
        )

        #print(str(access_token))
        return response_with(resp.SUCCESS_200, value={"access_token": access_token, "refresh_token": refresh_token}, message="Login successful.")
    else:
        return response_with(resp.UNAUTHORIZED_403, message="Invalid email or password.")

@user_routes.get('/')
@jwt_required()
def get_users():
    users = User.query.filter_by(school_id=g.school_id).all()
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    return response_with(resp.SUCCESS_200, value={"users": data})

@user_routes.get('/<int:user_id>')
@jwt_required()
def get_user(user_id):
    user = User.query.filter_by(school_id=g.school_id, id=user_id).first()
    if not user:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422, message="User not found")
    try: 
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return response_with(resp.SUCCESS_200, value={"user": data})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.SERVER_ERROR_500)

@user_routes.patch('/<int:user_id>')
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.filter_by(school_id=g.school_id, id=user_id).first()

    if not user:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422, message="User not found")

    try:
        user_schema = UserSchema(partial=True)
        user = user_schema.load(data, instance=user)
        db.session.commit()

        result = user_schema.dump(user)
        return response_with(resp.SUCCESS_200, value={"user": result}, message="User updated successfully")

    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500, message="Error updating user")

@user_routes.delete('/<int:user_id>')
@jwt_required()
def delete_user(user_id):
    user = User.query.filter_by(school_id=g.school_id, id=user_id).first()
    if not user:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422, message="User not found")

    try:
        db.session.delete(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, message="User deleted successfully")
    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500, message="Error deleting user")


@user_routes.post('/refresh')
@jwt_required(refresh=True)
def refresh_access_token():
    current_claims = get_jwt()
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity, additional_claims=current_claims)
    return response_with(resp.SUCCESS_200, value={"access_token": new_access_token}, message="Token refreshed successfully.")