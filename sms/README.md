# SMS Sending Service with Twilio and Express

This is a simple Node.js application using Express and the Twilio API to send SMS messages. It includes an API endpoint to send messages to specified phone numbers via HTTP requests.

## Prerequisites

- **Node.js** and **npm** installed on your machine.
- **Twilio account** with a valid Twilio phone number, Account SID, and Auth Token.

## Getting Started

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Set up Twilio credentials**:
   Replace `accountSid`, `authToken`, and `from` number in the code with your Twilio credentials and Twilio phone number.

## Code Overview

### Dependencies

- **Express**: Used to create a server and handle API requests.
- **CORS**: Allows cross-origin requests from different domains.
- **Twilio**: Provides the `twilio` library to connect to Twilio's API for sending SMS.

### Setting Up Express Server

- `app.use(cors())`: Enables CORS for all routes.
- `app.use(express.json())`: Parses incoming JSON requests.

### Twilio Client Setup

The `twilio` module requires `accountSid` and `authToken` to create a Twilio client instance for sending SMS messages.

### API Endpoints

#### POST /sendSMS

**Endpoint**: `/sendSMS`  
**Method**: `POST`

This endpoint receives a request with the recipient's phone number and the message body to send as an SMS.

- **Request Body**:

  ```json
  {
    "number": "+1234567890",
    "text": "Your message here"
  }
  ```

- **Response**:

  - **200 OK**: On successful message delivery, returns the message SID and status.

    ```json
    {
      "messageSid": "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "status": "Message sent successfully"
    }
    ```

  - **400 Bad Request**: If the `number` or `text` is missing in the request body.

    ```json
    {
      "message": "Number and text are required"
    }
    ```

  - **500 Internal Server Error**: If the message fails to send, returns an error message.

    ```json
    {
      "message": "Failed to send message",
      "error": "Error details here"
    }
    ```

### Running the Server

To start the server, run:

```bash
node app.js
```

The server listens on port `5555` by default or on a custom port defined in environment variables.

### Example Request

Use a tool like **curl** or **Postman** to test the endpoint:

```bash
curl -X POST http://localhost:5555/sendSMS \
-H "Content-Type: application/json" \
-d '{"number":"+1234567890", "text":"Hello from Twilio!"}'
```

## Error Handling

The application includes error handling for:

- Missing `number` or `text` parameters (400 status code).
- Twilio errors when sending messages (500 status code).
