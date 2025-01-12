import websocket
import json
import base64
from aud import audio

# WebSocket URL
WS_URL = "wss://45f1-2409-40e6-39-b8cd-c43f-9186-303-3ed9.ngrok-free.app/stream"

# Example audio payload (replace this with your actual Base64-encoded audio)

audio_payload = base64.b64encode(audio).decode('utf-8')

# Long input data
long_prompt = "Replace this with your long speech input data or use generated Base64 audio."

def on_open(ws):
    print("Connection opened.")

    # Send 'start' event
    start_event = {
        "event": "start",
        "streamSid": "test-stream-123",
        "connectionId": "connection-test-456",
        "tracks": ["inbound"]
    }
    ws.send(json.dumps(start_event))
    print("Sent start event.")

    # Send 'media' event with audio
    media_event = {
        "event": "media",
        "streamSid": "test-stream-123",
        "media": {
            "track": "inbound",
            "payload": audio_payload  # Replace with actual audio data
        }
    }
    ws.send(json.dumps(media_event))
    print("Sent media event.")

    # Simulate sending a long input
    user_input_event = {
        "event": "media",
        "streamSid": "test-stream-123",
        "media": {
            "track": "inbound",
            "payload": base64.b64encode(long_prompt.encode('utf-8')).decode('utf-8')
        }
    }
    ws.send(json.dumps(user_input_event))
    print("Sent user input event.")

def on_message(ws, message):
    print("Received message from server:", message)

def on_error(ws, error):
    print("Error occurred:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed.")

# Initialize WebSocket connection
ws = websocket.WebSocketApp(
    WS_URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# Run the WebSocket client
ws.run_forever()
