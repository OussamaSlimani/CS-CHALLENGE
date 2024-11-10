const twilio = require("twilio");

// Your Twilio credentials
const accountSid = "ACe727d7f79a44f9dca3bdd7215f53c6b2";
const authToken = "0fda98a56406f3f883eb0e6a51f9e9b4";

// Create Twilio client
const client = new twilio(accountSid, authToken);

// Send SMS
client.messages
  .create({
    body: "Hello, your password is dd54848",
    from: "+1 318 602 4957", // Your Twilio phone number
    to: "+21653381375", // Recipient's phone number
  })
  .then((message) => console.log(message.sid));
