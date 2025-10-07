"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    query_user = db.session.execute(select(User).where(
        User.email == email)).scalar_one_or_none()

    if query_user is None:
        return jsonify({"msg": "email does not exist"}), 404

    if not check_password_hash(query_user.password, password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"user_id": query_user.id, "user_logged": query_user.email, "access_token": access_token})


@api.route("/user", methods=["GET"])
def get_all_users():

    # Consulta todos los registros de una tabla
    all_users = db.session.execute(select(User)).scalars().all()
    # Procesar la info en un formato legible
    results = list(map(lambda item: item.serialize(), all_users))

    if results is None:
        return jsonify({"msg": "No hay usuarios"}), 404

    response_body = {"msg": "ok", "results": results}

    return jsonify(response_body), 200



@api.route("/signup", methods=["POST"])
def signup():
    request_body = request.json

    email = request_body.get("email", None)
    password = request_body.get("password", None)
 

    hashed_password = generate_password_hash(password) if password else None

    query_email = db.session.execute(select(User).where(
        User.email == email)).scalar_one_or_none()
    

    if query_email is not None:
        return jsonify({"msg": "Ya existe un usuario con ese email"}), 401
    if email is None:
        return jsonify({"msg": "El  email no puede estar vacío"}), 401
    if password is None:
        return jsonify({"msg": "La contraseña no puede estar vacía"}), 401
    

    new_user = User(
        email=email,
        password=hashed_password,
        
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario añadido correctamente", "new_user": new_user.serialize()})


