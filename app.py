from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
import bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_management"
mongo = PyMongo(app)

mongo.db.users.create_index("email", unique=True)

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
                "role": data["role"]
            }
        )
    except DuplicateKeyError:
        return jsonify({"message": "This email is already registered"}), 400

    return jsonify({"message": "User registered"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5002)
