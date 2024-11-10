const express = require("express");
const cors = require("cors");
const twilio = require("twilio");

// Your Twilio credentials
const accountSid = "ACe727d7f79a44f9dca3bdd7215f53c6b2";
const authToken = "0fda98a56406f3f883eb0e6a51f9e9b4";

// Create Twilio client
const client = new twilio(accountSid, authToken);

// Initialize Express app
const app = express();

// Use CORS middleware
app.use(cors());

// Middleware to parse JSON bodies
app.use(express.json());

// Send SMS endpoint
app.post("/sendSMS", async (req, res) => {
  const { number, text } = req.body;

  if (!number || !text) {
    return res.status(400).json({ message: "Number and text are required" });
  }

  try {
    const message = await client.messages.create({
      body: text,
      from: "+1 318 602 4957", // Your Twilio phone number
      to: number, // Recipient's phone number
    });

    res
      .status(200)
      .json({ messageSid: message.sid, status: "Message sent successfully" });
  } catch (error) {
    console.error(error);
    res
      .status(500)
      .json({ message: "Failed to send message", error: error.message });
  }
});

// Start the server
const PORT = process.env.PORT || 5555;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
