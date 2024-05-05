import React, { useState } from 'react';
import { StyleSheet, View, TextInput, Button, Text, Image, Modal } from 'react-native';

export default function PostScreen({ navigation, route }) {
  const { item, token } = route.params;
  const [caption, setCaption] = useState('');
  const [modalVisible, setModalVisible] = useState(true);

  function handlePost() {
    if (caption) {
      navigation.navigate('HomeScreen', { post: { ...item, caption } });
      setModalVisible(false);
      setCaption('');
    }
  }

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => {
        setModalVisible(!modalVisible);
      }}
    >
      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          <Text style={styles.heading}>Great song choice!</Text>
          <Image style={styles.largeImage} source={{ uri: item.album.images[0].url }} />
          <Text style={styles.title}>{item.name} - {item.artists.map(artist => artist.name).join(', ')}</Text>
          <TextInput
            style={styles.input}
            placeholder="Write a caption..."
            placeholderTextColor="#fff"  // White placeholder text
            value={caption}
            onChangeText={setCaption}
            maxLength={150}
          />
          <Button title="Post" color="#fff" onPress={handlePost} disabled={!caption.trim()} />
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    
    backgroundColor: '#070707',
  },
  modalView: {
    margin: 20,
    backgroundColor: 'black',  // Inverted background color
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
 
    elevation: 5,
  },
  input: {
    height: 40,
    width: '100%',
    marginVertical: 20,
    borderWidth: 1,
    borderColor: '#fff',  // Inverted border color
    padding: 10,
    color: '#fff',  // Inverted text color
    backgroundColor: '#000',  // Inverted input background
  },
  largeImage: {
    width: 200,
    height: 200,
    marginVertical: 20,
  },
  title: {
    fontSize: 16,
    color: '#fff',  // Inverted text color
  },
  heading: {
    fontSize: 20,
    fontWeight: 'bold',
    marginVertical: 10,
    color: '#fff',  // Inverted text color
  },
});
