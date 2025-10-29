from flask import Blueprint, request, jsonify
from src.api.utils.database import db
from src.api.models.admin import Admin
from src.api.schema.admin_schema import AdminSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

admin_routes = Blueprint("admin_routes", __name__)

@admin_routes.post('/')
def create_admin():
    data = request.get_json()
    admin_schema = AdminSchema()
    admin = admin_schema.load(data)
    try:
        result = admin_schema.dump(admin.create())
        return response_with(resp.SUCCESS_201, value={"admin": result})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.INVALID_INPUT_422, message=f"User may already exist!!!")

@admin_routes.post('/login')
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    admin = Admin.query.filter_by(email=email).first()
    if admin and admin.check_password(password):
        access_token = create_access_token(
            identity=admin.email,  # string identity
            additional_claims={"school_id": admin.school_id}
        )
        refresh_token = create_refresh_token(
            identity=admin.email,
            additional_claims={"school_id": admin.school_id}
        )

        #print(str(access_token))
        return response_with(resp.SUCCESS_200, value={"access_token": access_token, "refresh_token": refresh_token}, message="Login successful.")
    else:
        return response_with(resp.UNAUTHORIZED_403, message="Invalid email or password.")


@admin_routes.post('/refresh')
@jwt_required(refresh=True)
def refresh_access_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return response_with(resp.SUCCESS_200, value={"access_token": new_access_token}, message="Token refreshed successfully.")


@admin_routes.get("/debug")
@jwt_required()
def debug_token():
    # Get the main identity 
    identity = get_jwt_identity()
    
    # Get the full token claims
    claims = get_jwt()
    
    # Extract your custom claim
    school_id = claims.get("school_id")

    print("Decoded user:", identity)
    print("School ID:", school_id)

    return {
        "decoded_user": identity,
        "school_id": school_id,
        "all_claims": claims
    }, 200
