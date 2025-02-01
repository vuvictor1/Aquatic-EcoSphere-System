// Authors: Victor Vu and Jordan Morris
// File: app.js
// Description: Mobile app for Aquatic EcoSphere web app.
// Copyright (C) 2025 Victor V. Vu and Jordan Morris
// License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import React, { useEffect } from 'react';
import { SafeAreaView, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';
import { requestForToken, onMessageListener } from "./firebase";

const App = () => { // App component
  useEffect(() => {
    requestForToken()
      .then((token) => {
        console.log("FCM Token:", token);
        // Send the token to your server to store it
      })
      .catch((error) => console.error("Error requesting token:", error));

    onMessageListener()
      .then((payload) => {
        console.log("Message received: ", payload);
        // Show a notification or update the UI
      })
      .catch((err) => console.error("Error receiving message:", err));
  }, []);

  return ( 
    <SafeAreaView style={styles.container}> 
      <WebView // WebView component to display the web app
        source={{ uri: 'https://aquatic-eco.up.railway.app/' }} // use web app URL
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={true}
        allowsInlineMediaPlayback={true}
        mediaPlaybackRequiresUser Action={false}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({ // Set styles
  container: {
    flex: 1,
  },
  webview: {
    flex: 1,
  },
});

export default App; // export App component