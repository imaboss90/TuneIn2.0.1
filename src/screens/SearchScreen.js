import React, { useState } from 'react';
import { StyleSheet, View, TextInput, Button, FlatList, Text, Image, TouchableOpacity } from 'react-native';

export default function SearchScreen({ navigation, route }) {
  const { token } = route.params;
  const [search, setSearch] = useState('');
  const [results, setResults] = useState([]);

  async function searchTracks() {
    if (token && search) {
      try {
        const url = `https://api.spotify.com/v1/search?q=${encodeURIComponent(search)}&type=track&limit=5`;
        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setResults(data.tracks.items);
        } else {
          setResults([]);
          console.error('Error fetching search results:', response.status);
        }
      } catch (error) {
        setResults([]);
        console.error('Error fetching search results:', error);
      }
    } else {
      setResults([]);
    }
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Search tracks"
        placeholderTextColor="#fff"  // White placeholder text
        value={search}
        onChangeText={setSearch}
      />
      <Button title="Search" color="#fff" onPress={searchTracks} disabled={!search.trim()} />
      <FlatList
        data={results}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.item}
            onPress={() => navigation.navigate('PostScreen', { item, token })}
          >
            <Image style={styles.image} source={{ uri: item.album.images[0].url }} />
            <View style={styles.textContainer}>
              <Text style={styles.title} numberOfLines={2}>{item.name}</Text>
              <Text style={styles.artist}>{item.artists.map(artist => artist.name).join(', ')}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#000',  // Black background
  },
  input: {
    height: 40,
    width: '100%',
    marginVertical: 20,
    borderWidth: 1,
    borderColor: '#fff',  // White border
    padding: 10,
    color: 'white',  // White text on black background
    backgroundColor: 'black',  // Black input field background
    marginTop: 70,
  },
  item: {
    flexDirection: 'row',
    alignItems: 'flex-start', // Align start for proper text wrapping
    marginVertical: 8,
    marginBottom: 10,
    marginTop: 25,
  },
  image: {
    width: 80,
    height: 80,
    marginRight: 10,
    marginBottom: 25,
  },
  textContainer: {
    flex: 1, // Take up the remaining space
    marginLeft: 6,
  },
  title: {
    fontSize: 16,
    color: '#fff',  // White text
    marginBottom: 5,
  },
  artist: {
    fontSize: 14,
    color: '#ccc',  // Lighter grey text for artist names
  },
});
