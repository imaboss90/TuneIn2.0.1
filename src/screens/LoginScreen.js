import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text, TextInput, TouchableOpacity } from 'react-native';
import { makeRedirectUri, useAuthRequest } from 'expo-auth-session';
import base64 from 'base-64';

const discovery = {
  authorizationEndpoint: 'https://accounts.spotify.com/authorize',
  tokenEndpoint: 'https://accounts.spotify.com/api/token',
};

const client_id = '6f0688f887844b64bef2e6b742a6a327';
const client_secret = '789aeccf43284c1fb1f3dbc6a8a86f0d';

export default function LoginScreen({ navigation }) {
  const [token, setToken] = useState(null);
  const [request, response, promptAsync] = useAuthRequest(
    {
      clientId: client_id,
      scopes: ['user-read-email', 'user-library-read', 'playlist-read-private', 'user-read-recently-played'],
      usePKCE: false,
      redirectUri: makeRedirectUri({ useProxy: true }),
    },
    discovery
  );

  useEffect(() => {
    if (response?.type === 'success') {
      const { code } = response.params;
      fetchToken(code);
    }
  }, [response]);

  async function fetchToken(code) {
    const redirectUri = makeRedirectUri({ useProxy: true });
    const credentials = base64.encode(`${client_id}:${client_secret}`);
    const formBody = `code=${encodeURIComponent(code)}&redirect_uri=${encodeURIComponent(redirectUri)}&grant_type=authorization_code`;
    const response = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${credentials}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formBody
    });
    const responseData = await response.json();
    if (responseData.access_token) {
      setToken(responseData.access_token);
      navigation.navigate('DailyScreen', { token: responseData.access_token });
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>TuneIn</Text>
      <TouchableOpacity style={styles.buttonApple} onPress={() => {}}>
        <Text style={styles.buttonText}>LOG IN WITH APPLE</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.buttonSpotify} onPress={() => promptAsync()}>
        <Text style={styles.buttonText}>LOG IN WITH SPOTIFY</Text>
      </TouchableOpacity>
      <Text style={styles.label}></Text>
      <TextInput style={styles.input} placeholder="Email Address or Username" placeholderTextColor="#000" />
      <Text style={styles.label}></Text>
      <TextInput style={styles.input} placeholder="Password" secureTextEntry={true} placeholderTextColor="#000" />
      <Text style={styles.forgotPassword}>Forgot your password?</Text>
      <TouchableOpacity style={styles.buttonLogin} onPress={() => {}}>
        <Text style={styles.buttonTextLogin}>LOGIN</Text>
      </TouchableOpacity>
      <Text style={styles.signUp}>Or SIGN UP HERE</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000', // Adjust the background color
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
    color: '#fff', // Adjust the text color
  },
  input: {
    width: '80%',
    height: 40,
    marginBottom: 15,
    paddingLeft: 10,
    borderColor: '#ccc',
    borderWidth: 1,
    backgroundColor: '#fff',
    color: '#000',
  },
  label: {
    width: '80%',
    textAlign: 'left',
    marginBottom: 10,
    color: '#fff',
  },
  buttonApple: {
    backgroundColor: '#000',
    padding: 10,
    width: '80%',
    borderRadius: 5,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#fff',
  },
  buttonSpotify: {
    backgroundColor: '#1DB954', // Spotify color
    padding: 10,
    width: '80%',
    borderRadius: 5,
    marginBottom: 30,
  },
  buttonText: {
    color: '#fff',
    textAlign: 'center',
  },
  buttonLogin: {
    backgroundColor: '#fff',
    padding: 10,
    width: '80%',
    borderRadius: 5,
    marginBottom: 10,
  },
  buttonTextLogin: {
    color: '#000',
    textAlign: 'center',
  },
  forgotPassword: {
    marginTop: 20,
    color: '#fff',
    marginBottom: 10,
  },
  signUp: {
    color: '#fff',
    marginTop: 20,
  }
});
