# AI Electronics Sales Agent

An advanced AI-powered cold calling sales agent designed specifically for electronics sales. This application c![Untitled Diagram drawio](https://github.com/user-attachments/assets/ecc58d72-3c2d-432c-a172-34b127cb2f51)
ombines real-time voice interaction with customer data analysis to create personalized sales conversations. Built with Streamlit, it leverages speech-to-text, text-to-speech, and large language model capabilities to conduct natural sales conversations and track customer interactions.

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

## Prerequisites

- Python 3.7+
- PyAudio
- Streamlit
- MongoDB instance

## Required API Keys

The following API keys need to be set as environment variables:

```bash
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
MONGO_URL=your_mongodb_url
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

2. Start the application:
```bash
streamlit run main.py
```
3. The application will open in your default web browser
4. Load customer lists and sales targets
5. Allow microphone access when prompted
6. Monitor and manage sales calls in real-time
7. View conversation history and sales performance metrics
8. Access customer purchase history and preferences
9. Track successful sales and follow-up requirements

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

## File Structure

- `VoiceAgent.py`: Main application file containing Streamlit interface and voice agent logic
- `model.py`: Contains database models and interactions
- `prompt.py`: Defines conversation prompts and templates
- `functions.py`: Contains custom function definitions and mappings
- `customer_id.txt`: Stores current customer ID for personalization


## Error Handling

The application includes robust error handling for:
- WebSocket connections
- Audio stream management
- API calls
- Database operations
- Function execution
