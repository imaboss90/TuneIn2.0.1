import React, { useState, useEffect } from 'react';
import { StyleSheet, View, FlatList, Text, Image } from 'react-native';

export default function HomeScreen({ navigation, route }) {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    if (route.params?.post) {
      handlePostAdded(route.params.post);
    }
  }, [route.params?.post]);

  const handlePostAdded = (post) => {
    setPosts((prevPosts) => [...prevPosts, post]);
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={posts}
        keyExtractor={(item, index) => `${item.id}-${index}`}
        renderItem={({ item }) => (
          <View style={styles.postContainer}>
            <View style={styles.post}>
              <Image style={styles.image} source={{ uri: item.album.images[0].url }} />
              <View style={styles.postText}>
                <Text style={styles.title}>{item.name}</Text>
                <Text style={styles.artist}>{item.artists.map(artist => artist.name).join(', ')}</Text>
              </View>
            </View>
            <Text style={styles.caption}>{item.caption}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    alignItems: 'center',
    backgroundColor: 'black',
  },
  postContainer: {
    width: 332, // Maintain alignment by setting the width here
    marginTop: 35, // Space between posts
  },
  post: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#101010',
    borderRadius: 25,
    padding: 10,
    width: '100%', // Use 100% to fill container
    height: 132,
  },
  postText: {
    flex: 1,
    marginLeft: 10,
  },
  image: {
    width: 105,
    height: 105,
    borderRadius: 10,
    marginLeft: 10,
    marginRight: 10,
  },
  title: {
    fontSize: 25,
    color: 'white',
    marginBottom: 10,
  },
  artist: {
    fontSize: 18,
    color: 'white',
  },
  caption: {
    fontSize: 18,
    marginTop: 15,
    color: 'white',
    marginLeft: 12,
  },
});
