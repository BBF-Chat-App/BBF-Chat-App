from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app)

class APIRequestError(Exception):
    print("APIRequestError")

def api_call(endpoint, params=None, json=None, type="get"):
    # Specify the API endpoint URL
    # api_url = f"http://0.0.0.0:8000/{endpoint}"
    api_url = f"http://host.docker.internal:8000/{endpoint}"

    # Make a GET request to the API
    if type == "get":
        response = requests.get(api_url, params=params, json=json)
    if type == "post":
        response = requests.post(api_url, params=params, json=json)
    if type == "put":
        response = requests.put(api_url, params=params, json=json)
    if type == "delete":
        response = requests.delete(api_url, params=params, json=json)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and use the response data (assuming it's in JSON format)
        data = response.json()
        return data
    else:
        # Print an error message if the request was not successful
        raise APIRequestError(f"Error: {response.status_code} - {response.text}")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    username = request.form.get('username')
    return render_template('index.html', username=username)

@socketio.on('message')
def handle_message(data):
    # Save the message in the backend
    sender = data.get('username')
    message = data.get('message')
    
    api_call(endpoint="add_message", params={"message": message, "sender": sender}, type="post")

    # Broadcast the message to all connected clients
    socketio.emit('message', data)

    # Send updated messages to the current user
    updated_messages = api_call(endpoint="get_all_messages")
    socketio.emit('update_messages', {'messages': updated_messages})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
