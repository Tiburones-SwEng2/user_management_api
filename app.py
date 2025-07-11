from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flasgger import Swagger
from pymongo.errors import DuplicateKeyError
import bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from password_generator import PasswordGenerator
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_management"
mongo = PyMongo(app)
swagger = Swagger(app) 

mongo.db.users.create_index("email", unique=True)
app.config["JWT_SECRET_KEY"] = "lkhjap8gy2p 03kt"
jwt = JWTManager(app)
load_dotenv()

app.config.update(
    dict(
        MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
    )
)

mail = Mail(app)

@app.route('/register', methods=['POST'])
def register():
    """
    Registra al usuario en el sistema
    ---
    parameters:
        - in: body
          name: user_information
          schema:
            type: object
            required:
                - name
                - email
                - password
            properties:
                name:
                    type: string
                    example: Diego
                email:
                    type: string
                    example: prueba1@example.com
                password:
                    type: string
                    example: "12345678"
    
    responses:
        200:
            description: No hay informacion suficiente
        400:
            description: Este email ya esta registrado o el usuario ya esa registrado
    """
    data = request.get_json()
    
    if data["name"] == None or data["email"] == None or data["password"] == None:
        return jsonify({"mensaje": "No hay informacion suficiente"}), 400

    try:
        mongo.db.users.insert_one(
            {
                "name": data["name"],
                "email": data["email"],
                "password": bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()),
                "admin": "false"
            }
        )
    except DuplicateKeyError:
        return jsonify({"mensaje": "Este email ya esta registrado"}), 400

    return jsonify({"mensaje": "Usuario registrado"}), 200


@app.route('/login', methods=['POST'])
def login():
    """
    Permite que el usuario inicie sesion dentro del sistema
    ---
    parameters:
        - in: body
          name: user_login_information
          schema:
            type: object
            required:
                - email
                - password
            properties:
                email:
                    type: string
                    example: prueba1@example.com
                password:
                    type: string
                    example: "12345678"
    
    responses:
        200:
            description: login realizado correctamente
        400:
            description: Contraseña incorrecta
        404:
            description: El usuario no existe
    """
    data = request.get_json()

    user = mongo.db.users.find_one({"email": data["email"]})

    if user == None:
        return ({"mensaje": "El usuario no existe"}), 404

    if bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
         return jsonify(
                {
                    "name": user["name"],
                    "email": user["email"],
                    "admin": user["admin"],
                    "access_token": create_access_token(identity=user["email"])
                }
            ), 200
    else:    
        return jsonify({"mensaje": "Contraseña incorrecta"}), 400

@app.route('/recover', methods=['POST'])
def recover():
    """
    Permite que el usuario pueda generar una nueva contraseña en caso de que haya olvidado la original
    ---
    parameters:
        - in: body
          name: user_login_information
          schema:
            type: object
            required:
                - email
            properties:
                email:
                    type: string
                    example: prueba1@example.com
    
    responses:
        200:
            description: Constraseña entregada correctamente
        400:
            description: No se pudo enviar la contraseña
        404:
            description: El usuario no existe
    """
    data = request.get_json()

    user = mongo.db.users.find_one({"email": data["email"]})

    if user == None:
        return ({"mensaje": "El usuario no existe"}), 404

    new_pwd = PasswordGenerator().generate()

    mongo.db.users.update_one({"_id":user["_id"]}, {"$set": {"password": bcrypt.hashpw(new_pwd.encode("utf-8"), bcrypt.gensalt())}})


    msg = Message(
        subject="Recuperación de contraseña",
        sender=os.getenv('MAIL_USERNAME'),
        recipients=[data["email"]],
        body=f"""Hola, tu nueva contraseña es: {new_pwd}"""
    )

    try:
        mail.send(msg)
    except:
        return {"error": "No se pudo enviar la nueva contraseña"}, 400

    return {"mensaje": "La nueva contraseña fue entregada"}, 200
    
if __name__ == "__main__":
    app.run(debug=True, port=5002)
