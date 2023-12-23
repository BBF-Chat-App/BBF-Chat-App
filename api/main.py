import json
from confluent_kafka import Producer
from fastapi import FastAPI
from database import Connection


app = FastAPI()

# Edit the MongoDB connection string to connect your own database
db = Connection(uri="mongodb+srv://[username:password@]host[/[defaultauthdb][?options]]")

producer_conf = {
    'bootstrap.servers': 'kafka:29092',
    'client.id': 'my-app'
}

producer = Producer(producer_conf)


@app.post("/add_message")
def add_message(message, sender):
    try:
        # Serialize the dictionary to a JSON string
        message_data = json.dumps({"message": message, "sender": sender})

        try:
            # Pass the serialized JSON string as bytes to the produce method
            producer.produce('chat_messages', value=message_data.encode('utf-8'))
        except Exception as e:
            print(e)

        db.add_message(message=message, sender=sender)
        producer.flush()

        # Return the serialized JSON string in the response
        return {"status": "success", "message": {"message": message, "sender": sender}}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.get("/get_all_messages")
def get_all_messages():
    return db.get_all_messages()