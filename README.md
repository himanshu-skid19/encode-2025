![Untitled Diagram drawio](https://github.com/user-attachments/assets/ecc58d72-3c2d-432c-a172-34b127cb2f51)

# AI Electronics Sales Agent

An advanced AI-powered cold calling sales agent designed specifically for electronics sales. This application combines real-time voice interaction with customer data analysis to create personalized sales conversations. Built with Streamlit, it leverages speech-to-text, text-to-speech, and large language model capabilities to conduct natural sales conversations and track customer interactions.


## Features

- Automated cold calling for electronics sales
- Intelligent sales conversation management
- Customer purchase history tracking and analysis
- Personalized product recommendations
- Real-time voice interaction with AI
- Speech-to-text conversion using Deepgram
- Natural language processing using GPT models
- Text-to-speech synthesis with natural voice
- Live conversation display in Streamlit interface
- Support for custom sales functions and API integrations
- MongoDB integration for customer relationship management
- Detailed conversation history tracking
- Real-time audio streaming
- Sales performance analytics

## Demo Video
https://github.com/user-attachments/assets/13cf1a22-b8d3-4165-aa95-55834e6f105f

### Note:
We initially attempted to create the whole program in python with streamlit but faced difficulties in deploying our voice agent there. Thus, we converted our code to Javascript and Typescript to work with ReactJS and NodeJS to ease deployment. 
The structure of this repo is broadly divided into 4 sections:

1. ```Root```: which contains the main python code which is what we'd recommend running for local testing 
2. ```backend```: The code containing our backend made using NodeJS and MongoDB
3. ```voice-agent-ui```: the code for our voice agent demo deployed in NextJS
4. ```frontend```: the code for our dashboard for managing customer data



## Prerequisites

- Python 3.7+
- PyAudio
- Streamlit
- MongoDB instance

## Required API Keys

The following API keys need to be set as environment variables:

```bash
DEEPGRAM_API_KEY="INSERT DEEPGRAM KEY HERE"
OPENAI_API_KEY="INSERT OPENAI HERE"
GEMINI_API_KEY="INSERT GEMINIKEY HERE"
```

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

The application uses several configuration settings that can be modified:

- Voice Agent URL: `wss://agent.deepgram.com/agent`
- Voice Model: "aura-luna-en"
- STT Model: "nova-2"
- LLM Model: "gpt-4o-mini"
- Audio Settings:
  - Sample Rate: 16000 Hz
  - Encoding: linear16
  - Chunk Size: 0.05 seconds

## Usage

1. Set up your customer database in MongoDB with electronics product catalog and customer information
2. Go to https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn (create an account if you have not). Follow the steps to verify your whatsapp number and replace the auth_code and sid in the function success in the file functions.py. This basically sends the customer a feedback form link. The form is synced to google sheets which is synced to Mongodb through pythonanywhere.com. (This step is just for sending the form to your whatsapp number, you may skip it.)

3. Start the application:
```bash
streamlit run 1_Welcome.py
```
3. You will see two options : Customer ID :(Enter 9999 for testing, or insert a valid Customer entry in the database and enter their Customer ID)
4. Promt : You can enter the desired prompt for the LLM voice agent. Leaving it empty would default to the hard-coded prompt.
5. After entering the Customer ID and prompt(optional), click the VoiceAgent tab to chat with the agent.
6. You can also see and add entries in the MongoDB database.

### Sales Features

- Automatic customer profile loading
- Previous purchase history integration
- Product recommendation engine
- Customizable sales scripts and responses
- Real-time sales performance tracking
- Call outcome recording and analysis
- Follow-up scheduling automation

## Troubleshooting

- If experiencing audio issues, restart your computer, especially if you typically close your laptop instead of shutting down
- Use Postman to test API keys and endpoints
- Check if PortAudio is properly initialized
- Ensure all required environment variables are set
- Verify microphone permissions are granted to the application



## Error Handling

The application includes robust error handling for:
- WebSocket connections
- Audio stream management
- API calls
- Database operations
- Function execution


## Team Members
- Himanshu Singhal
- Ayush Kumar
- Anushka Gupta
- Rishita Agarwal
