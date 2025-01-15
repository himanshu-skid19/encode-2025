import pyaudio
import asyncio
import websockets
import os
import json
import threading
import janus
import queue
import sys
import requests
from anthropic import HUMAN_PROMPT, AI_PROMPT
import streamlit as st
import pyaudio
import asyncio
import websockets
import os
import json
import threading
import janus
import queue
import sys
from datetime import datetime
import pyaudio
import asyncio
import websockets
import os
import json
import threading
import janus
import queue
import sys
import requests
from anthropic import HUMAN_PROMPT, AI_PROMPT
import streamlit as st
import pyaudio
import asyncio
import websockets
import os
import json
import threading
import janus
import queue
import sys
from datetime import datetime
from langchain import hub
from dotenv import load_dotenv
from prompt import PROMPT
from functions import FUNCTION_DEFINITIONS, FUNCTION_MAP

VOICE_AGENT_URL = "wss://agent.deepgram.com/agent"


# os.environ["DEEPGRAM_API_KEY"] = "e8f6f8d073897bf83cd7856dc18cd3e6f0d3f503"
# os.environ["OPENAI_API_KEY"] = "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"




from dotenv import load_dotenv
import os
load_dotenv()


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Deepgram API Key:", DEEPGRAM_API_KEY)
print("OpenAI API Key:", OPENAI_API_KEY)


VOICE = "aura-luna-en"

LISTEN = "nova-2"

LLM_MODEL = "gpt-4o-mini"


USER_AUDIO_SAMPLE_RATE = 16000
USER_AUDIO_SECS_PER_CHUNK = 0.05
USER_AUDIO_SAMPLES_PER_CHUNK = round(USER_AUDIO_SAMPLE_RATE * USER_AUDIO_SECS_PER_CHUNK)

AGENT_AUDIO_SAMPLE_RATE = 16000
AGENT_AUDIO_BYTES_PER_SEC = 2 * AGENT_AUDIO_SAMPLE_RATE
from model import *


def format_purchases(products):
    """Format the purchases list into a readable string"""
    return "\n".join([f"- Product ID: {p['product_id']}, Purchased on: {p['date_bought'].strftime('%Y-%m-%d')}" 
                     for p in products])

mongoURL = os.getenv("MONGO_URL")

def get_prompt():
    """Create a personalized sales prompt from customer data"""
    with open("customer_id.txt", "r") as f:
        customer_id = f.read().strip()
    customer_data=get_customer_details(customer_id)
    new_prompt=PROMPT.format(
        name=customer_data['name'],
        customer_id=customer_data['customer_id'],
        customer_number=customer_data['customer_number'],
        formatted_purchases=format_purchases(customer_data['products']),
        has_previous_purchases=len(customer_data['products']) > 0
    )
    print("prompt: ", new_prompt)
    return new_prompt


SETTINGS = {
    "type": "SettingsConfiguration",
    "audio": {
        "input": {
            "encoding": "linear16",
            "sample_rate": USER_AUDIO_SAMPLE_RATE,
        },
        "output": {
            "encoding": "linear16",
            "sample_rate": AGENT_AUDIO_SAMPLE_RATE,
            "container": "none",
        },
    },
    "agent": {
        "listen": {
            "model": LISTEN
        },
       "think": {
      "provider": {
        "type": "open_ai"
      },
      "model": LLM_MODEL,
      "instructions": get_prompt(),
      "functions": FUNCTION_DEFINITIONS
    },
        "speak": {
            "model": VOICE
        },
    },
    # "context": {
    #     "messages": [], # LLM message history (e.g. to restore existing conversation if websocket connection breaks)
    #     "replay": False # whether to replay the last message, if it is an assistant message
    # }
}

class StreamlitSpeaker:
    
    def __init__(self):
        self._queue = None
        self._stream = None
        self._thread = None
        self._stop = None
        
    def __enter__(self):
        audio = pyaudio.PyAudio()
        self._stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=AGENT_AUDIO_SAMPLE_RATE,
            input=False,
            output=True,
        )
        self._queue = janus.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._play, 
            args=(self._queue, self._stream, self._stop), 
            daemon=True
        )
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stop.set()
        self._thread.join()
        self._stream.close()
        self._stream = None
        self._queue = None
        self._thread = None
        self._stop = None

    def _play(self, audio_out, stream, stop):
        while not stop.is_set():
            try:
                data = audio_out.sync_q.get(True, 0.05)
                stream.write(data)
            except queue.Empty:
                pass

    async def play(self, data):
        return await self._queue.async_q.put(data)

    def stop(self):
        if self._queue and self._queue.async_q:
            while not self._queue.async_q.empty():
                try:
                    self._queue.async_q.get_nowait()
                except janus.QueueEmpty:
                    break

def initialize_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'messages_container' not in st.session_state:
        st.session_state.messages_container = st.empty()

class VoiceAgent:
    def __init__(self):
        self.mic_audio_queue = asyncio.Queue()
        
    def audio_callback(self, input_data, frame_count, time_info, status_flag):
        self.mic_audio_queue.put_nowait(input_data)
        return (input_data, pyaudio.paContinue)

    async def run_agent(self):
        dg_api_key = os.environ.get("DEEPGRAM_API_KEY")
        if dg_api_key is None:
            st.error("DEEPGRAM_API_KEY env var not present")
            return

        async with websockets.connect(
            VOICE_AGENT_URL,
            extra_headers={"Authorization": f"Token {dg_api_key}"},
        ) as ws:
            async def microphone():
                audio = pyaudio.PyAudio()
                stream = audio.open(
                    format=pyaudio.paInt16,
                    rate=USER_AUDIO_SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=USER_AUDIO_SAMPLES_PER_CHUNK,
                    stream_callback=self.audio_callback,
                    channels=1
                )
                stream.start_stream()
                while stream.is_active():
                    await asyncio.sleep(0.1)
                stream.stop_stream()
                stream.close()

            async def sender(ws):
                await ws.send(json.dumps(SETTINGS))
                try:
                    while True:
                        data = await self.mic_audio_queue.get()
                        await ws.send(data)
                except Exception as e:
                    st.error(f"Error while sending: {str(e)}")
                    raise

            async def receiver(ws):
                try:
                    speaker = StreamlitSpeaker()
                    with speaker:
                        async for message in ws:
                            if isinstance(message, str):
                                print(message)
                                msg_data = json.loads(message)
                                if msg_data["type"] == 'Welcome':
                                    
                                    new_message = {
                                        "role": "assistant",
                                        "content":"Welcome ! How can I help you today?",
                                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                                    }
                                    st.session_state.conversation_history.append(new_message)
                                    render_conversation()
                                elif msg_data["type"] == 'ConversationText' and msg_data["role"] == "user":
                                    new_message = {
                                        "role": "user",
                                        "content": msg_data["content"],
                                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                                    }

                                   
                                    st.session_state.conversation_history.append(new_message)
                                    render_conversation()
                                
                                elif  (msg_data["type"] == "ConversationText" and msg_data["role"] == "assistant"):
                                    if msg_data.get("role") == "assistant":
                                        new_message = {
                                            "role": "assistant",
                                            "content": msg_data["content"],
                                            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
                                        }
                                        
                                        st.session_state.conversation_history.append(new_message)
                                        render_conversation()
                                        
                                
                                elif msg_data["type"] == "UserStartedSpeaking":
                                    speaker.stop()


                                elif msg_data["type"] == "FunctionCallRequest":
                                    
                                    function_name = msg_data["function_name"]
                                    function_args = msg_data["input"]
                                    
                                    function = FUNCTION_MAP.get(function_name)

                                    
                                    if function:
                                        
                                        result = await function(**function_args)
                                        print(result)
                                        print(result,msg_data["function_call_id"],'---------')
                                        await ws.send(json.dumps({
                                            "type": "FunctionCallResponse",
                                            "function_call_id": msg_data["function_call_id"],
                                            "output": str(result)
                                        }))

                            
                            elif isinstance(message, bytes):
                                await speaker.play(message)
                            
                except Exception as e:
                    st.error(f"Error in receiver: {str(e)}")

            await asyncio.wait([
                asyncio.ensure_future(microphone()),
                asyncio.ensure_future(sender(ws)),
                asyncio.ensure_future(receiver(ws))
            ])

def render_conversation():
    # Clear existing messages
    st.session_state.messages_container.empty()
    
    # Create a new container for messages
    with st.session_state.messages_container.container():
        for message in st.session_state.conversation_history:
            with st.chat_message(message["role"]):
                st.write(f"**{message['timestamp']}**")
                st.write(message["content"])

def main():
    st.set_page_config(page_title="Voice Assistant", page_icon="🎤", layout="wide")
    
    st.title("🎤 Voice Assistant")
    st.write("Speak to interact with the AI assistant. Your conversation will appear below in real-time.")
    
 
    initialize_session_state()
    

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Conversation")
        
        st.session_state.messages_container = st.empty()
        render_conversation()
    
    with col2:
        st.subheader("Status")
        status_placeholder = st.empty()
        status_placeholder.info("Listening...")
    
    
    try:
        agent = VoiceAgent()
        asyncio.run(agent.run_agent())
    except Exception as e:
        st.error(f"Error running voice agent: {str(e)}")

if __name__ == "__main__":
    main()