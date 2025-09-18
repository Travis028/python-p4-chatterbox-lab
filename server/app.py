from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


# ----------------------------
# GET /messages
# ----------------------------
@app.route('/messages', methods=["GET"])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return make_response(jsonify([m.to_dict() for m in messages]), 200)


# ----------------------------
# POST /messages
# ----------------------------
@app.route('/messages', methods=["POST"])
def create_message():
    data = request.get_json()

    if not data or "body" not in data or "username" not in data:
        return make_response(jsonify({"error": "Missing body or username"}), 400)

    new_message = Message(
        body=data["body"],
        username=data["username"]
    )
    db.session.add(new_message)
    db.session.commit()

    return make_response(jsonify(new_message.to_dict()), 201)


# ----------------------------
# PATCH /messages/<id>
# ----------------------------
@app.route('/messages/<int:id>', methods=["PATCH"])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if "body" in data:
        message.body = data["body"]

    db.session.commit()
    return make_response(jsonify(message.to_dict()), 200)


# ----------------------------
# DELETE /messages/<id>
# ----------------------------
@app.route('/messages/<int:id>', methods=["DELETE"])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return make_response(jsonify({"message": "Deleted successfully"}), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)