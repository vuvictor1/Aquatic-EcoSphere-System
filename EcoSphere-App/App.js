// Authors: Victor Vu and Jordan Morris
// File: app.js
// Description: Mobile app for Aquatic EcoSphere web app.
// Copyright (C) 2025 Victor V. Vu and Jordan Morris
// License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import React, { useEffect } from 'react';
import { SafeAreaView, StyleSheet, View, Alert } from 'react-native';
import { WebView } from 'react-native-webview';
import NativeNotify from 'native-notify';

const App = () => {
  useEffect(() => {
    // Initialize Native Notify
    NativeNotify.init({
      appId: 29538, // my Native Notify App ID from dashboard
      appToken: 'EZKmYk6xkadAq57gWH2MYZ', // my Native Notify App Token from dashboard
    });

    // Handle notification received
    NativeNotify.onNotificationReceived((notification) => {
      console.log('Notification Received:', notification);
      Alert.alert('Notification', notification.message);
    });

    // Handle notification response
    NativeNotify.onNotificationOpened((response) => {
      console.log('Notification Response:', response);
      Alert.alert('Notification Opened', response.message);
    });
  }, []);

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <WebView
          source={{ uri: 'https://aquatic-eco.up.railway.app/' }}
          style={styles.webview}
          javaScriptEnabled={true}
          domStorageEnabled={true}
          startInLoadingState={true}
          allowsInlineMediaPlayback={true}
          mediaPlaybackRequiresUserAction={false}
        />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#fff',
  },
  container: {
    flex: 1,
    marginTop: 35,
  },
  webview: {
    flex: 1,
  },
});

export default App;