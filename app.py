from flask import Flask, request, jsonify, render_template
from service import ChatService
from models import Schema
import json

app = Flask(__name__, static_folder='static')
chat_service = ChatService()

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/messages", methods=["GET"])
def get_messages():
    return jsonify(chat_service.get_messages())

@app.route("/api/messages", methods=["POST"])
def post_message():
    return jsonify(chat_service.post_message(request.get_json()))

@app.route("/api/users/rename", methods=["POST"])
def change_username():
    data = request.get_json()
    old_username = data.get("old_username")
    new_username = data.get("new_username")
    
    if not old_username or not new_username:
        return jsonify({"error": "Both old_username and new_username are required"}), 400
    
    result = chat_service.change_username(old_username, new_username)
    
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@app.route("/api/users/color", methods=["POST"])
def change_color():
    data = request.get_json()
    username = data.get("username")
    color = data.get("color")
    
    if not username or not color:
        return jsonify({"error": "Both username and color are required"}), 400
    
    return jsonify(chat_service.change_color(username, color))

@app.route("/api/users/<username>", methods=["GET"])
def get_user(username):
    user = chat_service.get_user(username)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Health check endpoint
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='0.0.0.0', port=5000)