# Voice Agent with Azure OpenAI Services

 [![Discord](https://dcbadge.vercel.app/api/server/xWRaCDBtW4?style=flat)](https://discord.gg/xWRaCDBtW4)

A basic example of using Deepgram's Voice Agent API with OpenAI Azure.

## Getting an API Key

🔑 To access the Deepgram API you will need a [free Deepgram API Key](https://console.deepgram.com/signup?jump=keys).

## Documentation

You can learn more about the Deepgram API at [developers.deepgram.com](https://developers.deepgram.com/docs).

## Installation

This is a Python client for interacting with Deepgram's Voice Agent API andd Azure OpenAI Services.

## Instructions

1. Install the dependencies in `requirements.txt`. For example, on Ubuntu using a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Set an environment variable with your Deepgram API key:

    ```bash
    export DEEPGRAM_API_KEY=<your-key-here>
    ```
3. Set an environment variable with your Azure OpenAI Services API key:

    ```bash
    export AZURE_OPENAI_API_KEY=<your-key-here>
    ```

3. Run the client:

    ```bash
    python3 client.py
    ```

4. Start talking into your mic. This client doesn't have echo cancellation; you'll want to use headphones so the agent doesn't hear itself and think it's user speech.


## Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](./.github/CODE_OF_CONDUCT.md). Then see the
[Contribution](./.github/CONTRIBUTING.md) guidelines for more information.

## Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue in this repository](https://github.com/deepgram/voice-agent-azure-open-ai-services/issues/new)
- [Join the Deepgram Github Discussions Community](https://github.com/orgs/deepgram/discussions)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)

[license]: LICENSE.txt
