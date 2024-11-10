const express = require("express");
const { AzureOpenAI } = require("openai");
const dotenv = require("dotenv");
const cors = require("cors"); // Import cors middleware

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Use CORS middleware to allow requests from any origin
app.use(cors());

// Middleware to parse JSON data
app.use(express.json());
app.use(express.static("public")); // Serve static files from 'public' folder

// Set up the Azure OpenAI client
const endpoint = process.env["AZURE_OPENAI_ENDPOINT"];
const apiKey = process.env["AZURE_OPENAI_API_KEY"];
const apiVersion = "2024-05-01-preview";
const deployment = "DeploymentGPT35T";
const client = new AzureOpenAI({ endpoint, apiKey, apiVersion, deployment });

// Route to handle chat requests
app.post("/chat", async (req, res) => {
  try {
    const userMessage = req.body.message;
    const result = await client.chat.completions.create({
      messages: [
        {
          role: "system",
          content:
            "You are a cybersecurity expert trained to give recommendations and advice on various cybersecurity measures. You will help users secure their computers and digital assets by providing actionable steps to prevent or mitigate potential cyber threats. Your responses should be clear, concise, and avoid technical jargon unless specifically requested by the user. If a question involves a complex scenario, break down your recommendations into easy-to-follow steps.\n\nYou are interacting with a user who is looking for help with securing their computer, dealing with potential malware, or managing their privacy online. The user might ask about best practices for securing accounts, handling suspicious emails, setting up firewalls, or preventing cyberattacks. Answer in a friendly and approachable manner, and where applicable, suggest actions based on common user security issues",
        },
        { role: "user", content: userMessage },
      ],
      max_tokens: 800,
      temperature: 0.7,
      top_p: 0.95,
    });

    const assistantResponse = result.choices[0].message.content;
    res.json({ response: assistantResponse });
  } catch (error) {
    console.error("Error in /chat route:", error);
    res
      .status(500)
      .json({ error: "An error occurred while processing your request." });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
