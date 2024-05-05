import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from './src/screens/LoginScreen';
import DailyScreen from './src/screens/DailyScreen';
import SearchScreen from './src/screens/SearchScreen';
import PostScreen from './src/screens/PostScreen';
import HomeScreen from './src/screens/HomeScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="LoginScreen"
          component={LoginScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="DailyScreen"
          component={DailyScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen name="SearchScreen" 
        component={SearchScreen} 
        options={{ headerShown: false }}/>

        <Stack.Screen name="PostScreen" 
        component={PostScreen} 
        options={{ headerShown: false }}/>

        <Stack.Screen name="HomeScreen" 
        component={HomeScreen}
        options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}