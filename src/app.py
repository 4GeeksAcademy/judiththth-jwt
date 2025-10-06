"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_cors import CORS

from sqlalchemy import select

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../dist/')
app = Flask(__name__)
app.url_map.strict_slashes = False

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


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file


@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


# --------------------------------------RUTAS LOGIN Y SIGNUP-----------------------------------

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # consulta en la tabla User que el email coincida con el que ha puesto el usuario
    query_user = db.session.execute(select(User).where(
        User.email == email)).scalar_one_or_none()
    # si devuelve None -> no encuentra el usuario.

    if query_user is None:
        return jsonify({"msg": "email does not exist"}), 404

    # si el email o la password no coincide con la bbdd, lanza error
    if email != query_user.email or password != query_user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"user_id": query_user.id, "user_logged": query_user.email, "access_token": access_token})


@app.route("/signup", methods=["POST"])
def signup():
    request_body = request.json

    username = request.json.get("username", None)
    name = request.json.get("name", None)
    surname = request.json.get("surname", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_active = request.json.get("is_active", None)

    # consulta en la tabla User que el email coincida con el que ha puesto el usuario
    query_email = db.session.execute(select(User).where(
        User.email == email)).scalar_one_or_none()
    query_username = db.session.execute(select(User).where(
        User.username == username)).scalar_one_or_none()
    # si devuelve None -> no encuentra el usuario.

    if query_email is not None:
        return jsonify({"msg": "Ya existe un usuario con ese email"}), 401
    if query_username is not None:
        return jsonify({"msg": "Ya existe un usuario con ese nombre de usuario"}), 401

    if request_body.get("username") is None:
        return jsonify({"msg": "El nombre de usuario no puede estar vacío"}), 401
    if request_body.get("name") is None:
        return jsonify({"msg": "El nombre no puede estar vacío"}), 401
    if request_body.get("surname") is None:
        return jsonify({"msg": "El apellido no puede estar vacío"}), 401
    if request_body.get("signup_date") is None:
        return jsonify({"msg": "El atributo signup_date no puede estar vacío"}), 401
    if request_body.get("email") is None:
        return jsonify({"msg": "El atributo email no puede estar vacío"}), 401
    if request_body.get("password") is None:
        return jsonify({"msg": "El atributo password no puede estar vacío"}), 401
    if request_body.get("is_active") is None:
        return jsonify({"msg": "El atributo is_active no puede estar vacío"}), 401

    new_user = User(
        username=request_body.get("username"),
        name=request_body.get("name"),
        surname=request_body.get("surname"),
        signup_date=request_body.get("signup_date"),
        email=request_body.get("email"),
        password=request_body.get("password"),
        is_active=request_body.get("is_active"),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Se ha añadido un usuario", "new_user": new_user.serialize()})


@app.route("/user", methods=["GET"])
def get_all_users():

    # ↓↓↓ Consultar todos los registros de una tabla, modelo o entidad
    all_users = db.session.execute(select(User)).scalars().all()
    # ↓↓↓ Se encarga de procesar la info en un formato legible para devs
    results = list(map(lambda item: item.serialize(), all_users))

    if results is None:
        return jsonify({"msg": "No hay usuarios"}), 404

    response_body = {"msg": "ok", "results": results}

    return jsonify(response_body), 200


@app.route("/user/<int:user_id>", methods=["GET"])
def get_one_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"msg": "El usuario no existe"}), 404

    response_body = {"msg": "ok", "result": user.serialize()}

    return jsonify(response_body), 200
