# Chat API with Azure OpenAI

This is a simple Express.js API that uses Azure's OpenAI to provide cybersecurity advice. Users can send questions related to cybersecurity, and the API will respond with helpful information.

## Setup

1. **Clone the repository** and navigate to the project folder.
2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Set up environment variables**: In a `.env` file, add:

   ```plaintext
   PORT=3000
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_API_KEY=your_azure_api_key
   ```

## Usage

1. **Start the server**:

   ```bash
   npm start
   ```

2. **Access the API** at `http://localhost:3000`.

## API Endpoints

- **POST /chat**: Send a JSON request with a "message" to receive a cybersecurity response.

  - Example request:

    ```json
    { "message": "How can I secure my computer?" }
    ```

  - Example response:

    ```json
    { "response": "To secure your computer, start by..." }
    ```

## Additional Notes

- CORS is enabled to allow cross-origin requests.
- Static files in the "public" folder are served at the root endpoint.
