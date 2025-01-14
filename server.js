// Import required modules
const fs = require("fs");
const http = require("http");
const path = require("path");
const dotenv = require("dotenv");
const { serpApiSearch } = require('./functions.js');
dotenv.config();

// Twilio
const HttpDispatcher = require("httpdispatcher");
const WebSocketServer = require("websocket").server;
const dispatcher = new HttpDispatcher();
const wsserver = http.createServer(handleRequest); // Create HTTP server to handle requests

const HTTP_SERVER_PORT = process.env.PORT || 8080; // Define the server port
let streamSid = ''; // Variable to store stream session ID

const mediaws = new WebSocketServer({
  httpServer: wsserver,
  autoAcceptConnections: true,
});

// Deepgram Speech to Text
const { createClient, LiveTranscriptionEvents } = require("@deepgram/sdk");
const deepgramClient = createClient(process.env.DEEPGRAM_API_KEY);
let keepAlive;

// OpenAI
const OpenAI = require('openai');
const openai = new OpenAI();

// Deepgram Text to Speech Websocket
const WebSocket = require('ws');
// const deepgramTTSWebsocketURL = 'wss://api.deepgram.com/v1/speak?encoding=mulaw&sample_rate=8000&container=none';
const deepgramTTSWebsocketURL = 'wss://api.deepgram.com/v1/speak?' + 
  new URLSearchParams({
    encoding: 'mulaw',
    sample_rate: 8000,
    container: 'none',
    model: 'aura-luna-en',  // Choose different model
  }).toString();

// Performance Timings
let llmStart = 0;
let ttsStart = 0;
let firstByte = true;
let speaking = false;
let send_first_sentence_input_time = null;
const chars_to_check = [".", ",", "!", "?", ";", ":"]

// Function to handle HTTP requests
function handleRequest(request, response) {
  try {
    dispatcher.dispatch(request, response);
  } catch (err) {
    console.error(err);
  }
}

/*
 Easy Debug Endpoint
*/
dispatcher.onGet("/", function (req, res) {
  console.log('GET /');
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello, World!');
});

/*
 Twilio streams.xml
*/
dispatcher.onPost("/twiml", function (req, res) {
  let filePath = path.join(__dirname + "/templates", "streams.xml");
  console.log(filePath);
  let stat = fs.statSync(filePath);
  // console.log("stat: ", stat);

  res.writeHead(200, {
    "Content-Type": "text/xml",
    "Content-Length": stat.size,
  });

  let readStream = fs.createReadStream(filePath);
  console.log("readStream: ", readStream);
  readStream.pipe(res);
});

/*
  Websocket Server
*/
mediaws.on("connect", function (connection) {
  console.log("twilio: Connection accepted");
  new MediaStream(connection);
});

/*
  Twilio Bi-directional Streaming
*/
class MediaStream {
  constructor(connection) {
    this.connection = connection;
    this.deepgram = setupDeepgram(this);
    this.deepgramTTSWebsocket = setupDeepgramWebsocket(this);
    connection.on("message", this.processMessage.bind(this));
    connection.on("close", this.close.bind(this));
    this.hasSeenMedia = false;

    this.messages = [];
    this.repeatCount = 0;
  }

  // Function to process incoming messages
  processMessage(message) {
    // console.log("twilio: message received");
    if (message.type === "utf8") {
      let data = JSON.parse(message.utf8Data);
      if (data.event === "connected") {
        console.log("twilio: Connected event received: ", data);
      }
      if (data.event === "start") {
        console.log("twilio: Start event received: ", data);
      }
      if (data.event === "media") {
        if (!this.hasSeenMedia) {
          console.log("twilio: Media event received: ", data);
          console.log("twilio: Suppressing additional messages...");
          this.hasSeenMedia = true;
        }
        if (!streamSid) {
          console.log('twilio: streamSid=', streamSid);
          streamSid = data.streamSid;
        }
        if (data.media.track == "inbound") {
          let rawAudio = Buffer.from(data.media.payload, 'base64');
          this.deepgram.send(rawAudio);
        }
      }
      if (data.event === "mark") {
        console.log("twilio: Mark event received", data);
      }
      if (data.event === "close") {
        console.log("twilio: Close event received: ", data);
        this.close();
      }
    } else if (message.type === "binary") {
      console.log("twilio: binary message received (not supported)");
    }
  }

  // Function to handle connection close
  close() {
    console.log("twilio: Closed");
  }
}

/*
  OpenAI Streaming LLM
*/
async function promptLLM(mediaStream, prompt) {
  console.log('openai LLM: prompt = ', prompt);
  
  const tools = [
    {
      type: "function",
      function: {
        name: "serpApiSearch",
        description: "Search the web using SerpApi's DuckDuckGo integration",
        parameters: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "The search query to look up",
            },
            maxResults: {
              type: "integer",
              description: "Maximum number of results to return (default: 5)",
              default: 5
            },
            region: {
              type: "string",
              description: "Search region/language code (default: us-en)",
              default: "us-en"
            }
          },
          required: ["query"],
        },
      },
    }
  ];

  const messages = [
    {
      role: 'assistant',
      content: `You are funny, everything is a joke to you.`
    },
    {
      role: 'user',
      content: prompt
    }
  ];

  try {
    speaking = true;
    let firstToken = true;
    let functionCallDetected = false;
    let accumulatedMessage = '';

    // First API call
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: messages,
      tools: tools,
      tool_choice: "auto",
      stream: true
    });

    for await (const chunk of response) {
      if (!speaking) break;

      if (firstToken) {
        const end = Date.now();
        const duration = end - llmStart;
        ttsStart = Date.now();
        console.warn('\n>>> openai LLM: Time to First Token = ', duration, '\n');
        firstToken = false;
        firstByte = true;
      }

      // Check for function calls
      if (chunk.choices[0]?.delta?.tool_calls) {
        functionCallDetected = true;
        break;
      }

      const chunk_message = chunk.choices[0]?.delta?.content || '';
      if (chunk_message) {
        accumulatedMessage += chunk_message;
        process.stdout.write(chunk_message);
        if (!send_first_sentence_input_time && containsAnyChars(chunk_message)) {
          send_first_sentence_input_time = Date.now();
        }
        
        try {
          await new Promise((resolve, reject) => {
            mediaStream.deepgramTTSWebsocket.send(
              JSON.stringify({ 'type': 'Speak', 'text': chunk_message }),
              (err) => err ? reject(err) : resolve()
            );
          });
        } catch (err) {
          console.error('Error sending to TTS websocket:', err);
        }
      }
    }

    // Handle function calling if detected
    if (functionCallDetected) {
      try {
        const functionResponse = await openai.chat.completions.create({
          model: 'gpt-4o-mini',
          messages: [...messages, { role: 'assistant', content: accumulatedMessage }],
          tools: tools,
          tool_choice: "auto",
        });

        const responseMessage = functionResponse.choices[0].message;
        
        if (responseMessage.tool_calls) {
          messages.push(responseMessage);

          // Execute SerpApi search with error handling
          const functionResponses = await Promise.all(
            responseMessage.tool_calls.map(async (toolCall) => {
              try {
                const functionArgs = JSON.parse(toolCall.function.arguments);
                const searchResults = await serpApiSearch(
                  functionArgs.query,
                  "11273a8046c26dedf404c4fc02c3fc0ecc0fd50a3f25373ac344c4ab2044a176",
                  {
                    maxResults: functionArgs.maxResults || 5,
                    region: functionArgs.region || 'us-en'
                  }
                );
                return {
                  tool_call_id: toolCall.id,
                  role: "tool",
                  name: toolCall.function.name,
                  content: JSON.stringify(searchResults)
                };
              } catch (error) {
                console.error('Error executing search:', error);
                return {
                  tool_call_id: toolCall.id,
                  role: "tool",
                  name: toolCall.function.name,
                  content: JSON.stringify([{ 
                    title: 'Error occurred',
                    url: '',
                    snippet: error.message
                  }])
                };
              }
            })
          );

          messages.push(...functionResponses);

          // Final streaming call with search results
          const finalStream = await openai.chat.completions.create({
            model: 'gpt-4o-mini',
            messages: messages,
            stream: true,
          });

          for await (const chunk of finalStream) {
            if (!speaking) break;

            const chunk_message = chunk.choices[0]?.delta?.content || '';
            if (chunk_message) {
              process.stdout.write(chunk_message);
              if (!send_first_sentence_input_time && containsAnyChars(chunk_message)) {
                send_first_sentence_input_time = Date.now();
              }
              
              try {
                await new Promise((resolve, reject) => {
                  mediaStream.deepgramTTSWebsocket.send(
                    JSON.stringify({ 'type': 'Speak', 'text': chunk_message }),
                    (err) => err ? reject(err) : resolve()
                  );
                });
              } catch (err) {
                console.error('Error sending to TTS websocket:', err);
              }
            }
          }
        }
      } catch (error) {
        console.error('Error in function calling:', error);
        // Send error message to TTS
        const errorMessage = "I apologize, but I encountered an error while searching. Let me continue without the search results.";
        await mediaStream.deepgramTTSWebsocket.send(JSON.stringify({ 'type': 'Speak', 'text': errorMessage }));
      }
    }
  } catch (error) {
    console.error('Error in promptLLM:', error);
    // Send error message to TTS
    const errorMessage = "I apologize, but I encountered an error. Please try again.";
    await mediaStream.deepgramTTSWebsocket.send(JSON.stringify({ 'type': 'Speak', 'text': errorMessage }));
  } finally {
    // Always send the Flush command, even if there was an error
    try {
      await mediaStream.deepgramTTSWebsocket.send(JSON.stringify({ 'type': 'Flush' }));
    } catch (err) {
      console.error('Error sending flush command:', err);
    }
  }
}

function containsAnyChars(str) {
  // Convert the string to an array of characters
  let strArray = Array.from(str);
  
  // Check if any character in strArray exists in chars_to_check
  return strArray.some(char => chars_to_check.includes(char));
}

/*
  Deepgram Streaming Text to Speech
*/
const setupDeepgramWebsocket = (mediaStream) => {
  const options = {
    headers: {
      Authorization: `Token ${process.env.DEEPGRAM_API_KEY}`
    }
  };
  const ws = new WebSocket(deepgramTTSWebsocketURL, options);

  ws.on('open', function open() {
    console.log('deepgram TTS: Connected');
  });

  ws.on('message', function incoming(data) {
    // Handles barge in
    // console.log('deepgram TTS: entered message');
    if (speaking) {
      // console.log("entered speaking");
      try {
        let json = JSON.parse(data.toString());
        // console.log('deepgram TTS: ', data.toString());
        return;
      } catch (e) {
        // Ignore
      }
      if (firstByte) {
        const end = Date.now();
        const duration = end - ttsStart;
        console.warn('\n\n>>> deepgram TTS: Time to First Byte = ', duration, '\n');
        firstByte = false;
        if (send_first_sentence_input_time){
          console.log(`>>> deepgram TTS: Time to First Byte from end of sentence token = `, (end - send_first_sentence_input_time));
        }
      }
      const payload = data.toString('base64');
      const message = {
        event: 'media',
        streamSid: streamSid,
        media: {
          payload,
        },
      };
      const messageJSON = JSON.stringify(message);

      // console.log('\ndeepgram TTS: Sending data.length:', data.length);
      mediaStream.connection.sendUTF(messageJSON);
    }
  });

  ws.on('close', function close() {
    console.log('deepgram TTS: Disconnected from the WebSocket server');
  });

  ws.on('error', function error(error) {
    console.log("deepgram TTS: error received");
    console.error(error);
  });
  return ws;
}

/*
  Deepgram Streaming Speech to Text
*/
const setupDeepgram = (mediaStream) => {
  console.log("deepgram STT: Setting up Deepgram STT");
  let is_finals = [];
  const deepgram = deepgramClient.listen.live({
    // Model
    model: "nova-2-phonecall",
    language: "en",
    // Formatting
    smart_format: true,
    // Audio
    encoding: "mulaw",
    sample_rate: 8000,
    channels: 1,
    multichannel: false,
    // End of Speech
    no_delay: true,
    interim_results: true,
    endpointing: 300,
    utterance_end_ms: 1000
  });

  if (keepAlive) clearInterval(keepAlive);
  keepAlive = setInterval(() => {
    deepgram.keepAlive(); // Keeps the connection alive
  }, 10 * 1000);

  deepgram.addListener(LiveTranscriptionEvents.Open, async () => {
    console.log("deepgram STT: Connected");

    deepgram.addListener(LiveTranscriptionEvents.Transcript, (data) => {
      const transcript = data.channel.alternatives[0].transcript;
      if (transcript !== "") {
        if (data.is_final) {
          is_finals.push(transcript);
          if (data.speech_final) {
            const utterance = is_finals.join(" ");
            is_finals = [];
            console.log(`deepgram STT: [Speech Final] ${utterance}`);
            llmStart = Date.now();
            promptLLM(mediaStream, utterance); // Send the final transcript to OpenAI for response
          } else {
            console.log(`deepgram STT:  [Is Final] ${transcript}`);
          }
        } else {
          console.log(`deepgram STT:    [Interim Result] ${transcript}`);
          if (speaking) {
            console.log('twilio: clear audio playback', streamSid);
            // Handles Barge In
            const messageJSON = JSON.stringify({
              "event": "clear",
              "streamSid": streamSid,
            });
            mediaStream.connection.sendUTF(messageJSON);
            mediaStream.deepgramTTSWebsocket.send(JSON.stringify({ 'type': 'Clear' }));
            speaking = false;
          }
        }
      }
    });

    deepgram.addListener(LiveTranscriptionEvents.UtteranceEnd, (data) => {
      if (is_finals.length > 0) {
        console.log("deepgram STT: [Utterance End]");
        const utterance = is_finals.join(" ");
        is_finals = [];
        console.log(`deepgram STT: [Speech Final] ${utterance}`);
        llmStart = Date.now();
        promptLLM(mediaStream, utterance);
      }
    });

    deepgram.addListener(LiveTranscriptionEvents.Close, async () => {
      console.log("deepgram STT: disconnected");
      clearInterval(keepAlive);
      deepgram.requestClose();
    });

    deepgram.addListener(LiveTranscriptionEvents.Error, async (error) => {
      console.log("deepgram STT: error received");
      console.error(error);
    });

    deepgram.addListener(LiveTranscriptionEvents.Warning, async (warning) => {
      console.log("deepgram STT: warning received");
      console.warn(warning);
    });

    deepgram.addListener(LiveTranscriptionEvents.Metadata, (data) => {
      console.log("deepgram STT: metadata received:", data);
    });
  });

  return deepgram;
};

wsserver.listen(HTTP_SERVER_PORT, function () {
  console.log("Server listening on: http://localhost:%s", HTTP_SERVER_PORT);
});
