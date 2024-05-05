import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';

export default function DailyScreen({ navigation, route }) {
  const { token } = route.params;

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={styles.tuneInButton}
        onPress={() => navigation.navigate('SearchScreen', { token })}
      >
        <Text style={styles.tuneInText}>Ready To TuneIn</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'black',
  },
  tuneInButton: {
    backgroundColor: 'black',
    borderRadius: 20,
    padding: 20,
  },
  tuneInText: {
    fontSize: 25,
    fontWeight: 'bold',
    color: 'white',
  },
});