from app import app
from models import db, Message

with app.app_context():
    # Clear existing data
    Message.query.delete()

    # Create sample messages
    messages = [
        Message(body="Hello, world!", username="admin"),
        Message(body="This is a test message", username="user1"),
        Message(body="Another message here", username="user2"),
        Message(body="Welcome to Chatterbox!", username="chatterbox"),
        Message(body="Testing the API", username="tester")
    ]

    db.session.add_all(messages)
    db.session.commit()
    print("Database seeded successfully!")