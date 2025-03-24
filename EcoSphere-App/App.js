// Authors: Victor Vu and Jordan Morris
// File: app.js
// Description: Mobile app for Aquatic EcoSphere web app.
// Copyright (C) 2025 Victor V. Vu and Jordan Morris
// License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import React from 'react';
import { SafeAreaView, StyleSheet, View } from 'react-native';
import { WebView } from 'react-native-webview';

const App = () => { // App component

  return ( // Uses SafeAreaView to avoid blocking front camera and other sensors
    <SafeAreaView style={styles.safeArea}> 
      <View style={styles.container}>
        <WebView // WebView component to display the web app
          source={{ uri: 'https://aquatic-eco.up.railway.app/' }} // use web app URL
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

const styles = StyleSheet.create({ // Set styles
  safeArea: {
    flex: 1,
    backgroundColor: '#fff', // set background color for the safe area
  },
  container: {
    flex: 1,
    marginTop: 35, // add vertical margin to avoid edges
  },
  webview: {
    flex: 1,
  },
});

export default App; // export App component