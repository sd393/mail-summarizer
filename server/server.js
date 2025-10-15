// server/server.js

const express = require('express');
const { OAuth2Client } = require('google-auth-library');
const cors = require('cors');
require('dotenv').config(); // This loads the .env file

const app = express();
const port = 8080; // Your backend will run on this port

// Use CORS middleware
app.use(cors());

// Initialize the Google OAuth client
const oAuth2Client = new OAuth2Client(
  process.env.CLIENT_ID,
  process.env.CLIENT_SECRET,
  'http://localhost:8080/auth/google/callback' // The backend redirect URI
);

// This is the endpoint that Google will redirect to after the user logs in
app.get('/auth/google/callback', async (req, res) => {
  const code = req.query.code;

  try {
    // Exchange the authorization code for an access token
    const { tokens } = await oAuth2Client.getToken(code);
    oAuth2Client.setCredentials(tokens);

    console.log('Successfully authenticated!');
    console.log('Access Token:', tokens.access_token);

    // Now you have the tokens. You should save them securely (e.g., in a database)
    // and then redirect the user back to your React app.

    // For now, let's just redirect them to the frontend's home page
    res.redirect('http://localhost:5173');

  } catch (error) {
    console.error('Error authenticating with Google:', error);
    res.status(500).send('Authentication failed');
  }
});

app.listen(port, () => {
  console.log(`✅ Server is running on http://localhost:${port}`);
});
