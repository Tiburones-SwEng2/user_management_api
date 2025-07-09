from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
import bcrypt
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_management"
mongo = PyMongo(app)

mongo.db.users.create_index("email", unique=True)
app.config["JWT_SECRET_KEY"] = "lkhjap8gy2p 03kt"
jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if data["name"] == None or data["email"] == None or data["password"] == None or data["role"] == None:
        return jsonify({"message": "Not enough information"}), 400

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
        return jsonify({"message": "This email is already registered"}), 400

    return jsonify({"message": "User registered"}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = mongo.db.users.find_one({"email": data["email"]})

    if user == None:
        return ({"message": "User does not exist"}), 404

    if bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
         return jsonify(
                {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                    "access_token": create_access_token(identity=user["email"])
                }
            ), 200
    else:    
        return jsonify({"message": "Incorrect password"}), 400

    
if __name__ == "__main__":
    app.run(debug=True, port=5002)
