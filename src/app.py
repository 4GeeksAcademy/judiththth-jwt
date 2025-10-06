"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, User
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import select

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../dist/')
jwt = None
app = Flask(__name__)
app.url_map.strict_slashes = False
jwt = JWTManager(app)
jwt = JWTManager(app)

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints



@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



@app.route("/login", methods=["POST"])
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


@app.route("/user", methods=["GET"])
def get_all_users():

    # Consulta todos los registros de una tabla
    all_users = db.session.execute(select(User)).scalars().all()
    # Procesar la info en un formato legible
    results = list(map(lambda item: item.serialize(), all_users))

    if results is None:
        return jsonify({"msg": "No hay usuarios"}), 404

    response_body = {"msg": "ok", "results": results}

    return jsonify(response_body), 200



@app.route("/signup", methods=["POST"])
def signup():
    request_body = request.json

    username = request_body.get("username", None)
    name = request_body.get("name", None)
    surname = request_body.get("surname", None)
    signup_date = request_body.get("signup_date", None)
    email = request_body.get("email", None)
    password = request_body.get("password", None)
    is_active = request_body.get("is_active", None)

    hashed_password = generate_password_hash(password) if password else None

    query_email = db.session.execute(select(User).where(
        User.email == email)).scalar_one_or_none()
    query_username = db.session.execute(select(User).where(
        User.username == username)).scalar_one_or_none()

    if query_email is not None:
        return jsonify({"msg": "Ya existe un usuario con ese email"}), 401
    if query_username is not None:
        return jsonify({"msg": "Ya existe un usuario con ese nombre de usuario"}), 401

    if username is None:
        return jsonify({"msg": "El nombre de usuario no puede estar vacío"}), 401
    if name is None:
        return jsonify({"msg": "El nombre no puede estar vacío"}), 401
    if surname is None:
        return jsonify({"msg": "El apellido no puede estar vacío"}), 401
    if signup_date is None:
        return jsonify({"msg": "La signup_date no puede estar vacía"}), 401
    if email is None:
        return jsonify({"msg": "El  email no puede estar vacío"}), 401
    if password is None:
        return jsonify({"msg": "La contraseña no puede estar vacía"}), 401
    if is_active is None:
        return jsonify({"msg": "is_active no puede estar vacío"}), 401

    new_user = User(
        username=username,
        name=name,
        surname=surname,
        signup_date=signup_date,
        email=email,
        password=hashed_password,
        is_active=is_active,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario añadido correctamente", "new_user": new_user.serialize()})
