const express = require('express');
const { OAuth2Client } = require('google-auth-library');
const cors = require('cors');
require('dotenv').config(); // This loads the .env file
const fs = require('fs').promises;
const path = require('path');
const { google } = require('googleapis');

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
    //Now, get users email.
    const oauth2 = google.oauth2({
      version: 'v2',
      auth: oAuth2Client,
    });
    const userInfoResponse = await oauth2.userinfo.get();
    const userEmail = userInfoResponse.data.email;
    console.log('User Email:', userEmail);

    //Write user email and access token to dictionary
    const tokenPath = path.join(__dirname, "..", "token.json");

    let allTokens = {};

    try {
      // Try to read the existing tokens file
      const data = await fs.readFile(tokenPath);
      allTokens = JSON.parse(data);
    } catch (error) {
      // File doesn't exist yet, it's fine. We'll create it.
      console.log('token.json not found, will create a new one.');
    }

    // Add or update the tokens for the current user
    allTokens[userEmail] = tokens;

    //Add or update client id and client secret
    client_id = process.env.CLIENT_ID;
    client_secret = process.env.CLIENT_SECRET;

    allTokens[userEmail]["client_id"] = client_id;
    allTokens[userEmail]["client_secret"] = client_secret;

    // No longer needed - write token information to token.json
    /*
    await fs.writeFile(tokenPath, JSON.stringify(allTokens, null, 2));
    console.log('Tokens saved to token.json');
    */

    //Send stuff to the database
    const { encryptJson } = require('./crypto');
    const { upsertUserByEmail, upsertUserToken } = require('./userRepo');

    const userId = await upsertUserByEmail(userEmail, 'free');

    const encrypted = encryptJson(allTokens[userEmail]);
    await upsertUserToken(userId, encrypted);


    // User redirected to home page.
    res.redirect('http://localhost:5173');

  } catch (error) {
    console.error('Error authenticating with Google:', error);
    res.status(500).send('Authentication failed');
  }
});

app.listen(port, () => {
  console.log(`✅ Server is running on http://localhost:${port}`);
});
