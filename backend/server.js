// server.js
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { createClient, AgentEvents } = require('@deepgram/sdk');
const mongoose = require('mongoose');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000", // Your React app's URL
    methods: ["GET", "POST"]
  },
  transports: ['websocket']
});

// Audio Configuration
const USER_AUDIO_SAMPLE_RATE = 16000;
const USER_AUDIO_SECS_PER_CHUNK = 0.05;
const USER_AUDIO_SAMPLES_PER_CHUNK = Math.round(USER_AUDIO_SAMPLE_RATE * USER_AUDIO_SECS_PER_CHUNK);

// Import Models
const Customer = require('./models/Customer');
const Product = require('./models/Product');
const Call = require('./models/Call');
const Survey = require('./models/Survey');

// Routes
app.use(cors());
app.use(express.json());
app.use('/api/customers', require('./routes/customers'));
app.use('/api/products', require('./routes/products'));
app.use('/api/calls', require('./routes/calls'));
app.use('/api/surveys', require('./routes/surveys'));

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || "mongodb+srv://himanshusinghal2003:pokemon123@legal.4rqce.mongodb.net/?retryWrites=true&w=majority&appName=legal", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('MongoDB Connected'))
.catch(err => console.error('MongoDB connection error:', err));

// Socket.IO Connection Handler
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  // Create Deepgram client
  const deepgram = createClient(process.env.DEEPGRAM_API_KEY);
  let connection = null;
  let audioBuffer = Buffer.alloc(0);
  let i = 0;

  // Setup Deepgram Agent
  const setupDeepgramAgent = async () => {
    try {
      connection = deepgram.agent();

      connection.on(AgentEvents.Open, async () => {
        console.log("Deepgram Connection opened");
        
        // Configure Deepgram Agent
        await connection.configure({
          audio: {
            input: {
              encoding: "linear16",
              sampleRate: USER_AUDIO_SAMPLE_RATE,
            },
            output: {
              encoding: "linear16",
              sampleRate: USER_AUDIO_SAMPLE_RATE,
              container: "wav",
            },
          },
          agent: {
            listen: {
              model: "nova-2",
            },
            speak: {
              model: "aura-asteria-en",
            },
            think: {
              provider: {
                type: "open_ai"
              },
              model: "gpt-4o-mini",
              instructions: "You are a helpful and engaging AI assistant."
            },
          },
        });
        console.log("Deepgram Agent configured");

        // Keep-alive interval
        const keepAliveInterval = setInterval(() => {
          console.log("Deepgram keep-alive");
          connection.keepAlive();
        }, 5000);

        // Cleanup on connection close
        connection.on(AgentEvents.Close, () => {
          console.log("Deepgram Connection closed");
          clearInterval(keepAliveInterval);
        });
      });

      // Handle conversation text
      connection.on(AgentEvents.ConversationText, async (data) => {
        console.log("Conversation text:", data);
        
        // Emit to client
        socket.emit('conversationText', {
          role: data.role || 'assistant',
          content: data.content
        });

        // Optionally log to file
        try {
          await fs.appendFile(
            path.join(__dirname, 'chatlog.txt'), 
            JSON.stringify(data) + "\n"
          );
        } catch (logError) {
          console.error('Error logging conversation:', logError);
        }

        // Store in MongoDB
        try {
          await new Call({
            transcribed_call: data.content,
            score: 1.0,
            customer_id: null
          }).save();
        } catch (error) {
          console.error('Error storing conversation:', error);
        }
      });

      // Handle audio output
      connection.on(AgentEvents.Audio, (data) => {
        const buffer = Buffer.from(data);
        audioBuffer = Buffer.concat([audioBuffer, buffer]);
        socket.emit('audioOutput', buffer);
      });

      // Handle agent audio completion
      connection.on(AgentEvents.AgentAudioDone, async () => {
        try {
          await fs.writeFile(
            path.join(__dirname, `output-${i}.wav`), 
            audioBuffer
          );
          audioBuffer = Buffer.alloc(0);
          i++;
        } catch (writeError) {
          console.error('Error writing audio file:', writeError);
        }
      });

      // Handle user started speaking (barge-in)
      connection.on(AgentEvents.UserStartedSpeaking, () => {
        if (audioBuffer.length) {
          console.log("Interrupting agent");
          audioBuffer = Buffer.alloc(0);
        }
      });

      // Handle errors
      connection.on(AgentEvents.Error, (error) => {
        console.error("Deepgram Error:", error);
        socket.emit('error', {
          message: 'Deepgram connection error',
          details: error.message
        });
      });

      // Handle metadata
      connection.on(AgentEvents.Metadata, (data) => {
        console.dir(data, { depth: null });
      });
    } catch (setupError) {
      console.error('Error setting up Deepgram agent:', setupError);
      socket.emit('error', {
        message: 'Failed to setup Deepgram agent',
        details: setupError.message
      });
    }
  };

  // Initial setup of Deepgram agent
  setupDeepgramAgent();

  // Handle audio input from client
  socket.on('audioInput', (audioChunk) => {
    try {
      if (connection) {
        connection.send(Buffer.from(audioChunk));
      } else {
        console.error('Deepgram connection not established');
        socket.emit('error', {
          message: 'Deepgram connection not established',
        });
      }
    } catch (error) {
      console.error('Error processing audio input:', error);
      socket.emit('error', {
        message: 'Failed to process audio input',
        details: error.message
      });
    }
  });

  // Handle client disconnection
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
    
    // Close Deepgram connection
    if (connection) {
      try {
        connection.removeAllListeners();
        connection.finish();
      } catch (disconnectError) {
        console.error('Error disconnecting Deepgram:', disconnectError);
      }
    }
  });
});

// Global error handling
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = { app, server, io };