import React, { useState, useEffect } from 'react';
import { StyleSheet, View, TextInput, Button, FlatList, Text, Image, TouchableOpacity, Modal, ScrollView } from 'react-native';
import { makeRedirectUri, useAuthRequest } from 'expo-auth-session';
import base64 from 'base-64';

const discovery = {
  authorizationEndpoint: 'https://accounts.spotify.com/authorize',
  tokenEndpoint: 'https://accounts.spotify.com/api/token',
};

const client_id = '6f0688f887844b64bef2e6b742a6a327';
const client_secret = '789aeccf43284c1fb1f3dbc6a8a86f0d';

function HomeScreen() {
  const [request, response, promptAsync] = useAuthRequest(
    {
      clientId: client_id,
      scopes: ['user-read-email', 'user-library-read', 'playlist-read-private', 'user-read-recently-played'],
      usePKCE: false,
      redirectUri: makeRedirectUri({ useProxy: true }),
    },
    discovery
  );

  const [token, setToken] = useState(null);
  const [search, setSearch] = useState('');
  const [results, setResults] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [caption, setCaption] = useState('');
  const [posts, setPosts] = useState([]);

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
    }
  }

  async function searchTracks() {
    if (token && search) {
      const url = `https://api.spotify.com/v1/search?q=${encodeURIComponent(search)}&type=track&limit=5`;
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setResults(data.tracks.items);
    }
  }

  function handleSelectTrack(item) {
    setSelectedTrack(item);
    setModalVisible(true);
  }

  function handlePost() {
    if (selectedTrack && caption) {
      setPosts(prevPosts => [...prevPosts, { ...selectedTrack, caption }]);
      setModalVisible(false);
      setCaption('');
    }
  }

  return (
    <ScrollView style={styles.container}>
      {!token && <Button title="Login to Spotify" onPress={() => promptAsync()} />}
      <TextInput
        style={styles.input}
        placeholder="Search tracks"
        value={search}
        onChangeText={setSearch}
        editable={!!token}
      />
      <Button title="Search" onPress={searchTracks} disabled={!token || !search.trim()} />
      <FlatList
        style={styles.list}
        data={results}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.item} onPress={() => handleSelectTrack(item)}>
            <Image style={styles.image} source={{ uri: item.album.images[0].url }} />
            <Text style={styles.title}>{item.name} - {item.artists.map(artist => artist.name).join(', ')}</Text>
          </TouchableOpacity>
        )}
      />
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(!modalVisible);
        }}>
        <View style={styles.centeredView}>
          <View style={styles.modalView}>
            <TextInput
              style={styles.input}
              placeholder="Enter a caption..."
              value={caption}
              onChangeText={setCaption}
            />
            <Button title="Post" onPress={handlePost} />
          </View>
        </View>
      </Modal>
      {posts.map((post, index) => (
        <View key={index} style={styles.post}>
          <Image style={styles.image} source={{ uri: post.album.images[0].url }} />
          <View style={styles.postText}>
            <Text style={styles.title}>{post.name}</Text>
            <Text>{post.artists.map(artist => artist.name).join(', ')}</Text>
            <Text>{post.caption}</Text>
          </View>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  input: {
    height: 40,
    width: '100%',
    marginVertical: 20,
    borderWidth: 1,
    padding: 10,
  },
  item: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 8,
  },
  image: {
    width: 50,
    height: 50,
    marginRight: 10,
  },
  title: {
    fontSize: 16,
  },
  list: {
    width: '100%'
  },
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
    width: 0,
    height: 2
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5
  },
  post: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'lightgray',
    borderRadius: 10,
    padding: 10,
    marginVertical: 8,
  },
  postText: {
    flex: 1,
    marginLeft: 10,
  }
});

export default HomeScreen;
