const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.get('/api/spotify-credentials', (req, res) => {
  const { CLIENT_ID, CLIENT_SECRET, REDIRECT_URI } = process.env;
  res.json({
    clientId: CLIENT_ID,
    clientSecret: CLIENT_SECRET,
    redirectUri: REDIRECT_URI
  });
});

app.post('/api/spotify-token', async (req, res) => {
  const { code } = req.body;
  const { CLIENT_ID, CLIENT_SECRET, REDIRECT_URI } = process.env;

  try {
    const response = await axios.post('https://accounts.spotify.com/api/token', null, {
      params: {
        grant_type: 'authorization_code',
        code,
        redirect_uri: REDIRECT_URI,
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
      },
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    const { access_token } = response.data;
    res.json({ access_token });
  } catch (error) {
    console.error('Failed to get Spotify access token:', error);
    res.status(500).json({ error: 'Failed to get Spotify access token' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});